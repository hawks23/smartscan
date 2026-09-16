
# SmartScan

**Turn medical documents into searchable text and AI-generated patient summaries.**

SmartScan is a Python application that processes medical PDFs and images through a simple Streamlit interface. It extracts text using Meta Llama through Amazon Bedrock, records document metadata, and consolidates the extracted information into a patient summary.

> **Status:** Prototype. Patient summaries are displayed in the app, and document metadata and OCR results are saved locally. Structured patient JSON is generated but currently only printed to the terminal.

## Features

- **Multiple document uploads** — Process PDF, JPG, JPEG, and PNG files.
- **Document preprocessing** — Convert PDF pages and supported images into JPEGs for OCR.
- **AI-powered text extraction** — Extract text from medical documents using Amazon Bedrock.
- **Metadata tracking** — Record filenames, file types, MIME types, file sizes, upload timestamps, and image paths.
- **Patient summaries** — Generate a consolidated overview of patient details, conditions, medications, and lab results, with model-generated assessments and suggested next steps.
- **Structured extraction** — Request a JSON representation of patient information and document metadata for further processing.

## How It Works

```text
Upload PDFs or images
         |
         v
Save files and register metadata
         |
         v
Convert documents into JPEG images
         |
         v
Extract text through Amazon Bedrock
         |
         v
Save metadata and OCR results
         |
         v
Generate a combined patient summary
         |
         v
Display the summary and request structured JSON
```

All documents in an upload batch are combined into one summary. Upload documents belonging to the same patient together.

## Technology Stack

| Component | Technology |
| --- | --- |
| Web interface | Streamlit |
| Application logic | Python |
| PDF rendering | PyMuPDF |
| Image processing | Pillow |
| AWS integration | Boto3 |
| OCR, summarization, and structured extraction | Meta Llama via Amazon Bedrock |
| Local storage | Filesystem and JSON files |

## Getting Started

### Prerequisites

- Python and pip
- Git
- AWS credentials configured for Boto3
- Access and invocation permissions for the configured Amazon Bedrock model
- An internet connection for Bedrock requests

The repository does not currently include a dependency manifest or pinned package versions.

### 1. Clone the Repository

```bash
git clone https://github.com/hawks23/smartscan.git
cd smartscan
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install streamlit boto3 PyMuPDF Pillow
```

### 4. Update the Pillow Resize Constant

The current code uses `Image.ANTIALIAS`, which was removed in Pillow 10.

In `secondary.py`, replace both occurrences of:

```python
img.thumbnail(max_size, Image.ANTIALIAS)
```

with:

```python
img.thumbnail(max_size, Image.Resampling.LANCZOS)
```

### 5. Configure AWS Access

Provide credentials through your usual Boto3-compatible AWS configuration, such as a shared credentials profile, environment variables, or an IAM role.

If the AWS CLI is installed, you can configure a local profile with:

```bash
aws configure
```

The source currently uses:

```text
Region:   us-east-1
Model ID: us.meta.llama3-2-90b-instruct-v1:0
```

These settings are defined in:

- `ocr.py`
- `llama_summary.py`
- `llama_extract.py`

Verify that the configured model is available to your AWS account. If you change the model or region, update all three files and use a model that supports image input for OCR.

### 6. Launch the App

Run this command from the repository root:

```bash
python -m streamlit run main.py
```

Open the local URL printed by Streamlit.

## Usage

1. Upload one or more supported documents for a single patient.
2. Wait while the app converts the documents, extracts text, and generates a summary.
3. Read the **Patient Summary** displayed in the app.
4. Inspect the generated registry files for document metadata and extracted text.
5. Check the terminal for processing messages and the structured extraction response.

Processing begins automatically after upload.

## Outputs

| Output | Location | Description |
| --- | --- | --- |
| Original documents | `uploads/` | Copies of uploaded files |
| Processed images | `images/<document-name>/` | JPEGs generated from PDFs and images |
| Document registry | `document_registry.json` | Metadata and generated image paths |
| OCR registry | `document_registry_with_ocr.json` | Metadata with extracted text for each image |
| Patient summary | Streamlit interface | Combined summary of uploaded documents |
| Structured patient data | Terminal output | Model-generated JSON text |

The code for saving structured patient data to `registry_metadata.json` is commented out in `main.py`. This file is not produced by the current application, and the generated response is not automatically validated as JSON.

## Project Structure

```text
smartscan/
├── main.py                         # Streamlit interface and processing workflow
├── secondary.py                    # Document registry and image preprocessing
├── ocr.py                          # Image-to-text extraction through Bedrock
├── llama_summary.py                # Patient summary generation
├── llama_extract.py                # Structured patient data extraction
├── document_registry.json          # Document metadata
├── document_registry_with_ocr.json # Metadata and OCR results
├── example.json                    # Example JSON file
├── uploads/                        # Uploaded documents
└── images/                         # Processed document images
```

## Current Limitations

- The app creates a fresh in-memory registry on each Streamlit run; it does not automatically reload previous registry files.
- Registry JSON files are overwritten during processing. Reusing filenames can also overwrite uploaded files and generated images.
- Transparent or palette-based PNGs may require conversion to RGB before processing because the code saves images as JPEG.
- Processing is sequential, with no background queue or progress tracking.
- The summary is displayed as text. Editable fields and color-coded results mentioned in the model prompt are not implemented as interface features.
- OCR and generated summaries can contain errors or inferred information.

## Data Handling

Uploaded files, processed images, and registry data are stored locally. Document images and extracted text are sent to Amazon Bedrock, and generated summaries and structured output are printed to the terminal.

Use synthetic or de-identified documents when evaluating the prototype. Generated medical interpretations and suggested next steps require review by a qualified healthcare professional.

## License

No license file is currently included in the repository.
````
