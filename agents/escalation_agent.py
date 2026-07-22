from google.adk.agents import Agent

escalation_agent = Agent(
    model="gemini-flash-latest",
    name="escalation_agent",
    description="Produces the final escalation decision.",

    instruction="""
    Use all previous results:

    SOAP Notes:
    {soap_notes}

    Symptom Retrieval:
    {symptom_results}

    Triage:
    {triage_result}

    Apply these rules:

    - Emergency:
      Immediate healthcare professional review.

    - Needs Doctor:
      Recommend doctor consultation.

    - Normal:
      Provide general non-diagnostic advice.

    Return one final response containing:

    1. SOAP Notes
    2. Identified Symptoms and Qdrant Results
    3. Triage Classification
    4. Escalation Status
    5. Disclaimer that this does not replace professional diagnosis
    """,

    output_key="final_result",
)