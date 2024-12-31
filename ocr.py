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
        - input_tokens: int, number of input tokens used.
        - output_tokens: int, number of output tokens used.
        """
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
                        {"text": "extract the text in that image"},
                    ],
                }
            ]

            # Send the request to Bedrock model
            response = self.bedrock_runtime.converse(
                modelId=self.model_id,
                messages=messages,
            )

            # Extract token usage details from response metadata (if available)
            input_tokens = int(response["usage"]["inputTokens"])
            output_tokens = int(response["usage"]["outputTokens"])

            # Extract the response text
            response_text = response["output"]["message"]["content"][0]["text"]

            return response_text, input_tokens, output_tokens

        except Exception as e:
            print(f"An error occurred while processing {image_path}: {e}")
            return "", 0, 0

    def process_images_in_folder(self, folder_path, output_folder):
        """
        Processes all images in a folder to extract text and save it to the output folder.
        
        Parameters:
        - folder_path: str, path to the folder containing images.
        - output_folder: str, path to the folder where OCR results will be saved.
        
        Returns:
        - token_counts: dict, containing input tokens, output tokens, and total tokens.
        """
        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Placeholder for token counts
        total_input_tokens = 0
        total_output_tokens = 0

        # Loop over all files in the folder
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)

            # Ensure the file is an image
            if not (filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg") or filename.lower().endswith(".png")):
                continue  # Skip non-image files

            # Extract text from the image
            response_text, input_tokens, output_tokens = self.extract_text_from_image(image_path)

            # Update token counts
            total_input_tokens += input_tokens
            total_output_tokens += output_tokens

            # Save the extracted text to the output folder
            ocr_output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(ocr_output_path, "w", encoding="utf-8") as f:
                f.write(response_text)

        # Prepare token count summary
        token_counts = {
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
        }

        return token_counts
