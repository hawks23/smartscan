# main.py
import streamlit as st
from secondary import DocumentRegistry
import os
from mimetypes import guess_type

# Initialize the document registry
registry = DocumentRegistry()

# Title of the app
st.title("Document Metadata Registry")

# Ensure the uploads directory exists
os.makedirs("uploads", exist_ok=True)

# Ensure the images directory exists
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
    registry.process_ocr_for_registry()

    # Save updated registry with OCR data
    registry.save_registry("document_registry.json")
    st.success("OCR processing completed and saved!")
