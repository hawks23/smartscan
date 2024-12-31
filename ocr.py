# package/ocr.py
import boto3
from PIL import Image
import io
import os

class OCRProcessor:
    def __init__(self, model_id="us.meta.llama3-2-90b-instruct-v1:0", region_name="us-east-1"):
        self.model_id = model_id
        self.bedrock_runtime = boto3.client("bedrock-runtime", region_name=region_name)

    def extract_text_from_image(self, image_path):
        """
        Extract text from a single image using the Bedrock model.
        
        Parameters:
        - image_path: str, path to the image file.
        
        Returns:
        - response_text: str, text extracted from the image.
        """
        print(f"Performing OCR on image: {image_path}")
        try:
            # Open and process the image
            with Image.open(image_path) as img:
                img = img.resize((800, 800), Image.LANCZOS)

                # Convert the image to bytes
                with io.BytesIO() as output:
                    img.save(output, format='JPEG')
                    image_bytes = output.getvalue()

            # Prepare the messages payload for the model
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"image": {"format": "jpeg", "source": {"bytes": image_bytes}}}, 
                        {"text": "The following is a medical document containing lab results. This could be a presecription, a lab report, or a medical record. Perform OCR and Extract the text from the image. Be sure to not make any mistakes in the extraction. Do not include any special characters or symbols. Return ONLY the text extracted from the image and no other comments."},
                    ],
                }
            ]

            # Send the request to Bedrock model
            response = self.bedrock_runtime.converse(
                modelId=self.model_id,
                messages=messages,
            )

            # Extract the response text
            response_text = response["output"]["message"]["content"][0]["text"]

            return response_text

        except Exception as e:
            print(f"An error occurred while processing {image_path}: {e}")
            return ""
