from google.adk.agents import Agent

triage_agent = Agent(
    model="gemini-flash-latest",
    name="triage_agent",
    description="Classifies patient urgency.",

    instruction="""
    Review the retrieved symptom information:

    {symptom_results}

    Classify the patient into exactly one category:

    - Normal
    - Needs Doctor
    - Emergency

    Use the highest severity when multiple symptoms are present.

    Return the category and a brief reason.
    """,

    output_key="triage_result",
)