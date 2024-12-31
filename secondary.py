# secondary.py
import os
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image
import shutil

class DocumentRegistry:
    def __init__(self):
        self.registry = []

    def add_document(self, filename, file_type, mime_type, file_size):
        metadata = {
            "Original Filename": filename,
            "File Type": file_type,
            "MIME Type": mime_type,
            "File Size": file_size,
            "Upload Timestamp": datetime.now().isoformat(),
            "Images": []
        }
        self.registry.append(metadata)
        return metadata

    def update_document_with_images(self, filename, images):
        for doc in self.registry:
            if doc["Original Filename"] == filename:
                doc["Images"] = images
                print(f"Updated document '{filename}' with images: {images}")
                break

    def get_registry(self):
        return self.registry

    def save_registry(self, file_path):
        import json
        with open(file_path, 'w') as f:
            json.dump(self.registry, f, indent=4)

    def load_registry(self, file_path):
        import json
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.registry = json.load(f)

    @staticmethod
    def convert_pdf_to_images(pdf_path, base_output_dir, max_size=(1000, 1000)):
        try:
            # Create a dedicated folder for the images of this PDF
            pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
            pdf_output_dir = os.path.join(base_output_dir, pdf_name)

            # Clear the folder if it exists
            if os.path.exists(pdf_output_dir):
                shutil.rmtree(pdf_output_dir)

            # Recreate the folder
            os.makedirs(pdf_output_dir, exist_ok=True)

            # Open the PDF file
            pdf_document = fitz.open(pdf_path)
            image_paths = []

            for page_num in range(pdf_document.page_count):
                # Get the page
                page = pdf_document.load_page(page_num)

                # Convert the page to an image
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Resize the image if it exceeds the max_size
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.ANTIALIAS)

                # Define image file name, e.g., "page_1.jpg"
                image_filename = os.path.join(pdf_output_dir, f"page_{page_num + 1}.jpg")
                img.save(image_filename, 'JPEG')
                image_paths.append(image_filename)

            pdf_document.close()
            return image_paths

        except Exception as e:
            print(f"An error occurred while processing '{pdf_path}': {e}")
            return []

    @staticmethod
    def process_image_file(image_path, base_output_dir, max_size=(1000, 1000)):
        print("Processing image file:", image_path)
        try:
            # Create a dedicated folder for the image
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            image_output_dir = os.path.join(base_output_dir, image_name)

            # Clear the folder if it exists
            if os.path.exists(image_output_dir):
                shutil.rmtree(image_output_dir)

            # Recreate the folder
            os.makedirs(image_output_dir, exist_ok=True)

            # Open and process the image
            img = Image.open(image_path)

            # Resize the image if it exceeds the max_size
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.ANTIALIAS)

            # Save the processed image
            processed_image_path = os.path.join(image_output_dir, f"{image_name}.jpg")
            img.save(processed_image_path, 'JPEG')

            print(f"Processed and saved image: {processed_image_path}")
            return [processed_image_path]

        except Exception as e:
            print(f"An error occurred while processing '{image_path}': {e}")
            return []

    def process_file(self, file_path, base_output_dir, max_size=(1000, 1000)):
        print(f"Processing file: {file_path}")
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".pdf":
            images = self.convert_pdf_to_images(file_path, base_output_dir, max_size)
        elif file_extension in [".jpg", ".jpeg", ".png"]:
            images = self.process_image_file(file_path, base_output_dir, max_size)
        else:
            print(f"Unsupported file type: {file_extension}")
            images = []

        # Ensure the images list updates the registry
        self.update_document_with_images(os.path.basename(file_path), images)
        print(f"Processing completed for file: {file_path}")
