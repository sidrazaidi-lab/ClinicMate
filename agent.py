from google.adk.agents import SequentialAgent

from agents.soap_agent import soap_agent
from agents.symptom_agent import symptom_agent
from agents.triage_agent import triage_agent
from agents.escalation_agent import escalation_agent


root_agent = SequentialAgent(
    name="clinicmate",

    description="""
    ClinicMate processes doctor-patient conversations,
    generates SOAP notes, retrieves symptom information,
    performs triage, and decides escalation.
    """,

    sub_agents=[
        soap_agent,
        symptom_agent,
        triage_agent,
        escalation_agent,
    ],
)