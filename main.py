# main.py
import streamlit as st
from secondary import DocumentRegistry
from llama_summary import generate_summary
import os
from mimetypes import guess_type

# Initialize the document registry
registry = DocumentRegistry()

# Title of the app
st.title("Document Metadata Registry with OCR Summarization")

# Ensure required directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("images", exist_ok=True)

# File uploader
uploaded_files = st.file_uploader("Upload your documents", accept_multiple_files=True)

# Save metadata and process files
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_size = uploaded_file.size
        file_type = os.path.splitext(file_name)[1].strip('.')
        mime_type, _ = guess_type(file_name)

        # Save file locally
        save_path = os.path.join("uploads", file_name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Add metadata to the registry
        registry.add_document(file_name, file_type, mime_type, file_size)

        # Process the file (PDFs and image files)
        output_dir = "images"
        registry.process_file(save_path, output_dir)

    # Perform OCR on all documents with images
    print("Performing OCR on uploaded documents...")
    registry.process_ocr_for_registry()
    print("OCR processing completed.")

    # Save updated registry with OCR data
    registry.save_registry("document_registry_with_ocr.json")
    print("Updated registry saved with OCR data.")

    # Automatically generate a summary
    print("Starting summarization of OCR data...")
    combined_ocr_text = registry.get_combined_ocr_for_all_documents()

    if combined_ocr_text.strip():
        summary = generate_summary(combined_ocr_text)
        print("Summarization completed.")
        st.success("OCR processing and summarization completed!")

        # Display the summary in the app
        st.subheader("Patient Summary")
        st.text(summary)
    else:
        print("No OCR data available for summarization.")
        st.warning("No OCR data available for summarization. Please upload valid documents.")
