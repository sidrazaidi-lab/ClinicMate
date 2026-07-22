# ClinicMate

ClinicMate is a multi-agent healthcare assistant built using Google ADK, Qdrant, Gemini, and Streamlit.

## Features

- Converts doctor-patient conversations into SOAP notes
- Extracts symptoms
- Retrieves medical information from Qdrant
- Classifies cases as Normal, Needs Doctor, or Emergency
- Escalates serious cases to healthcare professionals

## Workflow

Patient Conversation  
→ SOAP Agent  
→ Symptom Agent  
→ Qdrant Retrieval  
→ Triage Agent  
→ Escalation Agent

## Run the Project

Install dependencies:

```bash
pip install -r requirements.txt