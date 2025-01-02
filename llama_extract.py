# llama_summary.py
import boto3
from botocore.exceptions import ClientError
import textwrap
import json

# Bedrock model configuration
MODEL_ID = "us.meta.llama3-2-90b-instruct-v1:0"
REGION_NAME = "us-east-1"

# Initialize Bedrock runtime client
bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION_NAME)

# summary = """Patient Summary
# **Patient Details**

# * **Name**: PRATHAPA CHANDRA VARMA
# * **Age/Gender**: 70 Years / Male
# * **Unique ID**: MBLC3843
# * **Primary Care Physician**: Dr. P N VARMA
# * **Last Visit Date**: 04-May-2023

# **Health Snapshot**

# * **Active Conditions**:
# * **Anemia**:
# - **Year of Diagnosis**: Not available
# - **Severity Level**: Mild (Hb: 12.4 gm/dl)
# - **Management Status**: Needs Review
# - **Next Steps**: Suggest iron supplements, follow-up blood tests to monitor Hb levels
# * **Inflammation**:
# - **Year of Diagnosis**: Not available
# - **Severity Level**: Moderate (CRP: 5.0 mg/L)
# - **Management Status**: Controlled
# - **Next Steps**: Continue monitoring CRP levels, consider anti-inflammatory medication if necessary
# * **Current Medications**:
# * **Medication details unavailable**
# * **Recent Lab Results**:
# * **Complete Haemogram**:
# - **Haemoglobin (HB)**: 12.4 gm/dl (Normal: 13.0-16.0 gm/dl)
# - **Total WBC Count (TC)**: 8,070 /cumm (Normal: 4,000-10,000 /cumm)
# - **Differential Count (DC)**:
# - **Neutrophils**: 65.4% (Normal: 40-80%)
# - **Lymphocytes**: 23.8% (Normal: 20-40%)
# - **Eosinophils**: 5.7% (Normal: 0-6%)
# - **Monocytes**: 4.5% (Normal: 4.5-5.5%)
# - **Basophils**: 0.6% (Normal: 0-1%)
# * **Electrolytes**:
# - **Sodium**: 140 mEq/L (Normal: 136-145 mEq/L)
# - **Potassium**: 4.9 mEq/L (Normal: 3.5-5.1 mEq/L)
# - **Chloride**: 102 mEq/L (Normal: 95-108 mEq/L)
# - **Bicarbonate**: 29 mEq/L (Normal: 22-30 mEq/L)
# * **C-Reactive Protein (CRP)**: 5.0 mg/L (Normal: < 10 mg/L)

# **Guidelines for Severity, Management, and Next Steps**

# * **Severity Assessment**:
# - Anemia: Mild
# - Inflammation: Moderate
# * **Management Status**:
# - Anemia: Needs Review
# - Inflammation: Controlled
# * **Next Steps**:
# - Anemia: Suggest iron supplements, follow-up blood tests to monitor Hb levels
# - Inflammation: Continue monitoring CRP levels, consider anti-inflammatory medication if necessary"""

def summary_extract(summary: str) -> str:
    print("Summary Extract")
    """
    Generates a concise summary and actionable recommendations for given text (e.g., lab test results).
    
    Parameters:
    - extracted_text: str, text extracted from OCR data to summarize.
    
    Returns:
    - str: The generated summary and recommendations.
    """
    # Construct the prompt for Bedrock API
    try:
        with open("document_registry.json", 'r') as file:
            json_data = json.load(file)
            # Convert the entire JSON content into a string
            json_string = json.dumps(json_data, indent=4)
            print("JSON Data found")
    except FileNotFoundError:
        return f"Error: The file was not found."
    except json.JSONDecodeError:
        return "Error: The file is not a valid JSON file."
    
    # Create prompt as a string
    prompt = textwrap.dedent(f""" 
    The following are two documents. A json file that contains information about patient documents and a summary of the contents on the patient documents.
    You are an expert in reading given information and reformatting the same for building software. Study the data from the json file and summary and reformat it and fill in the empty tags below :
    {{
        "Patient Information": {{
            "Patient Name": "",
            "Patient ID": "",
            "Age/Gender": "",
            "Primary Care Physician": "",
            "Last Visit": ""
        }},
        "Documents": [
            {{
                "Original Filename": "",
                "File Type": "",
                "MIME Type": "",
                "File Size": ,
                "Upload Timestamp": "",
                "Images": [
                    "",
                    "",
                    "",
                    "",
                    ""
                ]
            }},
            {{
                "Original Filename": "",
                "File Type": "",
                "MIME Type": "",
                "File Size": ,
                "Upload Timestamp": "",
                "Images": [
                    ""
                ]
            }},
            {{
                "Original Filename": "",
                "File Type": "",
                "MIME Type": "",
                "File Size": ,
                "Upload Timestamp": "",
                "Images": [
                    ""
                ]
            }}
        ],
        "Active Conditions": [
            {{
                "Condition Name": "",
                "Diagnosed": "",
                "Management Status": "",
                "Next Steps": ""
            }},
            {{
                "Condition Name": "",
                "Diagnosed": "",
                "Management Status": "",
                "Next Steps": ""
            }}
        ],
        "Current Medications": [
            {{
                "Medication Name": "",
                "Dosage": "",
                "Frequency": "",
                "Start Date": ""
            }},
            {{
                "Medication Name": "",
                "Dosage": "",
                "Frequency": "",
                "Start Date": ""
            }}
        ],
        "Recent Lab Results": [
            {{
                "Test Name": "",
                "Date": "",
                "Result": "",
                "Normal Range": "",
                "Status": "",
                "Severity": "",
                "Management Status": "",
                "Next Steps": ""
            }},
            {{
                "Test Name": "",
                "Date": "",
                "Result": "",
                "Normal Range": "",
                "Status": "",
                "Severity": "",
                "Management Status": "",
                "Next Steps": ""
            }},
            {{
                "Test Name": "",
                "Date": "",
                "Result": "",
                "Normal Range": "",
                "Status": "",
                "Severity": "",
                "Management Status": "",
                "Next Steps": ""
            }}
        ],
        "Guidelines": [
            {{
                "Type": "",
                "Reference": "",
                "Link": ""
            }},
            {{
                "Type": "",
                "Reference": "",
                "Link": ""
            }}
        ],
        "Notes": ""
    }}

    Document registry : {json_string},
    Summary : {summary}

    (for example :
    {{
        "Patient Information": {{
            "Patient Name": "PRATHAPA CHANDRA VARMA",
            "Patient ID": "MBLC3843",
            "Age/Gender": "70 Years / Male",
            "Primary Care Physician": "Dr. P N VARMA",
            "Last Visit": "04-May-2023"
        }},
        "Documents": [
            {{
                "Original Filename": "PRATHAPA CHANDRA VARMA-2.pdf",
                "File Type": "pdf",
                "MIME Type": "application/pdf",
                "File Size": 651067,
                "Upload Timestamp": "2025-01-02T10:58:33.648331",
                "Images": [
                    "images\\PRATHAPA CHANDRA VARMA-2\\page_1.jpg",
                    "images\\PRATHAPA CHANDRA VARMA-2\\page_2.jpg",
                    "images\\PRATHAPA CHANDRA VARMA-2\\page_3.jpg",
                    "images\\PRATHAPA CHANDRA VARMA-2\\page_4.jpg",
                    "images\\PRATHAPA CHANDRA VARMA-2\\page_5.jpg"
                ],
            }},
            {{
                "Original Filename": "PRATHAPA CHANDRA VARMA-2_page_1.jpg",
                "File Type": "jpg",
                "MIME Type": "image/jpeg",
                "File Size": 75649,
                "Upload Timestamp": "2025-01-02T10:58:33.831955",
                "Images": [
                    "images\\PRATHAPA CHANDRA VARMA-2_page_1\\PRATHAPA CHANDRA VARMA-2_page_1.jpg"
                ]
            }},
            {{
                "Original Filename": "PRATHAPA CHANDRA VARMA-2_page_2.jpg",
                "File Type": "jpg",
                "MIME Type": "image/jpeg",
                "File Size": 63133,
                "Upload Timestamp": "2025-01-02T10:58:33.856733",
                "Images": [
                    "images\\PRATHAPA CHANDRA VARMA-2_page_2\\PRATHAPA CHANDRA VARMA-2_page_2.jpg"
                ]
            }}
        ],
        "Active Conditions": [
            {{
                "Condition Name": "Hypertension",
                "Diagnosed": "2020",
                "Management Status": "Controlled",
                "Next Steps": "Adjust antihypertensive medication"
            }}
        ],
        "Current Medications": [
            {{
                "Medication Name": "Metformin",
                "Dosage": "500 mg",
                "Frequency": "Twice daily",
                "Start Date": "Jan 2020"
            }},
            {{
                "Medication Name": "Amlodipine",
                "Dosage": "5 mg",
                "Frequency": "Once daily",
                "Start Date": "May 2018"
            }}
        ],
        "Recent Lab Results": [
            {{
                "Test Name": "HbA1c",
                "Date": "04-May-2023",
                "Result": "7.2%",
                "Normal Range": "< 6.5%",
                "Status": "High",
                "Severity": "Moderate",
                "Management Status": "Needs Review",
                "Next Steps": "Increase medication dosage and conduct follow-up test."
            }},
            {{
                "Test Name": "LDL Cholesterol",
                "Date": "04-May-2023",
                "Result": "160 mg/dL",
                "Normal Range": "< 100 mg/dL",
                "Status": "High",
                "Severity": "Severe",
                "Management Status": "Uncontrolled",
                "Next Steps": "Prescribe statins and recommend dietary changes."
            }},
            {{
                "Test Name": "C-Reactive Protein (CRP)",
                "Date": "04-May-2023",
                "Result": "5.0 mg/L",
                "Normal Range": "< 10 mg/L",
                "Status": "Normal",
                "Severity": "Low",
                "Management Status": "Controlled",
                "Next Steps": "Continue monitoring."
            }}
        ],
        "Guidelines": [
            {{
                "Type": "Cardiology",
                "Reference": "AHA/ACC Hypertension Guidelines",
                "Link": "https://www.heart.org/"
            }},
            {{
                "Type": "Endocrinology",
                "Reference": "ADA Diabetes Standards",
                "Link": "https://www.diabetes.org/"
            }}
        ],
        "Notes": "All extracted information has been consolidated. Recommendations and insights should be reviewed by a healthcare professional."
    }}
    )
    The task is to fill in the empty tags in the json file with the data from the summary. Fields which require medical expertise can be filled in using your medical knowledge.
    Undestand that the number of recent lab results and active conditions can vary. Fill in the data accordingly
    Return only the text after filling in the empty tags and combining the data from the json file and the summary as told above.
    **REMEMBER** to return the data as JSON string with NO OTHER ADDITIONS. This will be directy saved as a JSON file and should not contain any unnecessary comments or mistakes in formatting.
    """)

    try:
        # Send the request to Bedrock model
        print("Extracting the data from the text")
        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=[{
                "role": "user",
                "content": [{"text": prompt}]
            }],
        )

        # Extract and return response text
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
        # prompt = textwrap.dedent(f"""Verify and validate the formatting of the following JSON text and return only the corrected json, which will be saved as a json file directly.
        # json text : {response_text}
        # """)
        # try:
        #     # Send the request to Bedrock model
        #     print("Extracting the data from the text")
        #     response = bedrock_runtime.converse(
        #         modelId=MODEL_ID,
        #         messages=[{
        #             "role": "user",
        #             "content": [{"text": prompt}]
        #         }],
        #     )

        #     # Extract and return response text
        #     response_text = response["output"]["message"]["content"][0]["text"]
        #     # print("Generated Extract:\n", response_text)
        #     return response_text
        # except ClientError as e:
        #     print(f"ERROR: Failed to invoke model '{MODEL_ID}': {e}")
        # return "Error: Unable to generate validate json."

    except ClientError as e:
        print(f"ERROR: Failed to invoke model '{MODEL_ID}': {e}")
        return "Error: Unable to generate summary."
    except Exception as e:
        print(f"ERROR: Unexpected error occurred: {e}")
        return "Error: An unexpected error occurred while generating the summary."

