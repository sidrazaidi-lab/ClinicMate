from google.adk.agents import Agent

soap_agent = Agent(
    model="gemini-flash-latest",
    name="soap_agent",
    description="Generates SOAP notes from the conversation.",

    instruction="""
    Convert the doctor-patient conversation into SOAP notes.

    Include:

    Subjective:
    Objective:
    Assessment:
    Plan:

    Do not invent vital signs or test results.
    """,

    output_key="soap_notes",
)