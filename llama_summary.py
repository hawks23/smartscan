# llama_summary.py
import boto3
from botocore.exceptions import ClientError
import textwrap

# Bedrock model configuration
MODEL_ID = "us.meta.llama3-2-90b-instruct-v1:0"
REGION_NAME = "us-east-1"

# Initialize Bedrock runtime client
bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION_NAME)


def generate_summary(extracted_text: str) -> str:
    """
    Generates a concise summary and actionable recommendations for given text (e.g., lab test results).

    Parameters:
    - extracted_text: str, text extracted from OCR data to summarize.

    Returns:
    - str: The generated summary and recommendations.
    """
    # Construct the prompt for Bedrock API
    # prompt = textwrap.dedent(f"""
    #     <|begin_of_text|><|start_header_id|>system<|end_header_id|> 
    #     You are a medical assistant at a healthcare facility. You have received the following lab test results for a patient. 
    #     Greet the patient by name, provide a concise summary of their health based on the test results, and suggest actionable recommendations.

    #     Lab Test Results: {extracted_text}
        
    #     Summarize the results and provide recommendations. Be clear, concise, and actionable.
    #     <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    # """)

    prompt = textwrap.dedent(f"""## Comprehensive Health Snapshot Report Generator

    ### Introduction
    - **YOU ARE** a **MEDICAL DATA ANALYST** specializing in consolidating patient health information into actionable insights for healthcare providers.

    (Context: "Your expertise ensures accuracy and clarity in summarizing critical patient information for clinical use.")

    ### Task Description
    - **YOUR TASK IS** to **ANALYZE** a patient's health data and **GENERATE** a structured summary in line with the provided attributes and requirements.

    (Context: "This summary will guide clinicians in assessing patient health, managing conditions, and planning next steps effectively.")

    ---

    ### Data Attributes to Extract and Format
    #### 1. **Header Information**
    - **PATIENT DETAILS**: Extract name, age/gender, unique ID, primary care physician, and last visit date.
    - **MISSING DATA CLARIFICATION**: If last visit is unavailable, display "No recent visit recorded" and prompt scheduling or updating patient details.

    #### 2. **Health Snapshot**
    - **ACTIVE CONDITIONS**:
        - **Condition Name**
        - **Year of Diagnosis** (if available)
        - **Severity Level**:
        - Use clinical thresholds (e.g., hypertension: mild < 140/90 mm Hg; diabetes: controlled HbA1c < 6.5%) or suggest placeholders if data is insufficient.
        - **Management Status**:
        - Classify as Controlled, Needs Review, or Uncontrolled using available data like vitals, labs, and adherence reports.
        - **Next Steps**:
        - Suggest actions such as medication adjustment, additional tests, or lifestyle changes, with caveats for clinician validation.

    - **CURRENT MEDICATIONS**:
        - Extract and display name, dosage, frequency, and start date. If incomplete, use "Medication details unavailable" and provide editable fields for updating.

    - **RECENT LAB RESULTS**:
        - Include test name, date, result, normal range, and status (e.g., normal, high, low). Highlight abnormal values using color codes.

    #### 3. **Guidelines for Severity, Management, and Next Steps**
    - **SEVERITY ASSESSMENT**:
        - Perform assessments based on clinical thresholds and patient-specific factors. Be accurate and consistent in severity classification.
    - **MANAGEMENT STATUS**:
        - Base classifications on adherence to clinical guidelines and patient-specific baselines.
    - **NEXT STEPS**:
        - Offer actionable recommendations aligned with condition management protocols, ensuring clinician review. The clinician must be given good reccomendations and helpful points to proceed with the patient.

    #### 4. **Formatting and Presentation**
    - Organize data into headings and subheadings for clarity.
    - Add **editable fields** for missing data to enable clinician updates.

    ---

    ### Goals and Constraints
    - **ENSURE** the summary is **ACCURATE**, **CLINICALLY RELEVANT**, and **EASY TO INTERPRET**.
    - **YOU MUST AVOID** including speculative or unverified information without clear caveats.
    - **USE** standard clinical terminology and guidelines for consistency and precision.
    - **RETURN** only the summarized data and nothing else. Do not speak about the prompt or the underlying system.

    ---

    ### Outcome Expectations
    - **PROVIDE** a consolidated summary with:
    - Complete patient details.
    - Comprehensive health snapshots (active conditions, severity, medications, lab results).
    - Clear caveats for missing or inferred data.
    - **INCLUDE** placeholders for clinician inputs where data is unavailable.

    (Context: "This ensures clinicians receive actionable insights while maintaining flexibility for updates.")

    ---

    ### IMPORTANT
    - "Your insights directly impact patient care quality—accuracy and clarity are paramount."
    - "This task requires your attention to detail and adherence to clinical relevance."
    - Display only upto "Guidelines for Severity, Management, and Next Steps". Do not display **Formatting and Presentation**, **Goals and Constraints** and **Outcome Expectations** sections in output.
                             
    Lab OCR Data: {extracted_text}
    """)

    try:
        # Send the request to Bedrock model
        print("Summarizing OCR data...")
        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ],
        )

        # Extract and return response text
        response_text = response["output"]["message"]["content"][0]["text"]
        print("Generated Summary:\n", response_text)
        return response_text

    except ClientError as e:
        print(f"ERROR: Failed to invoke model '{MODEL_ID}': {e}")
        return "Error: Unable to generate summary."
    except Exception as e:
        print(f"ERROR: Unexpected error occurred: {e}")
        return "Error: An unexpected error occurred while generating the summary."
