import asyncio
import sys
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


PROJECT_DIR = Path(__file__).resolve().parent

# Load Gemini API key from my_agent/.env
load_dotenv(PROJECT_DIR / ".env")

PARENT_DIR = PROJECT_DIR.parent

if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from my_agent.agent import root_agent


# ---------------------------------------------------------
# STREAMLIT PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="ClinicMate",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 ClinicMate")

st.write(
    "AI-powered clinical documentation, symptom retrieval, "
    "patient triage, and escalation."
)


# ---------------------------------------------------------
# RUN THE GOOGLE ADK AGENT
# ---------------------------------------------------------

async def analyse_conversation(conversation: str) -> str:
    """Send the conversation through the complete ADK workflow."""

    app_name = "clinicmate"
    user_id = "streamlit_user"
    session_id = str(uuid.uuid4())

    # Create a temporary session for this analysis.
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    # Connect the Streamlit app to the ADK root agent.
    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service,
    )

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(text=conversation)
        ],
    )

    final_response = ""

    # Run the SequentialAgent workflow.
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    ):
        if event.is_final_response() and event.content:
            response_parts = []

            for part in event.content.parts:
                if getattr(part, "text", None):
                    response_parts.append(part.text)

            if response_parts:
                final_response = "\n".join(response_parts)

    if not final_response:
        final_response = (
            "The agent completed the request but did not return "
            "a final text response."
        )

    return final_response


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

conversation = st.text_area(
    "Enter the doctor-patient conversation",
    height=220,
    placeholder=(
        "Doctor: What brings you in today?\n"
        "Patient: I have chest pain and breathing difficulty."
    ),
)


# ---------------------------------------------------------
# ANALYSE BUTTON
# ---------------------------------------------------------

if st.button(
    "Analyze Conversation",
    type="primary",
    use_container_width=True,
):
    if not conversation.strip():
        st.warning("Please enter a doctor-patient conversation.")

    else:
        with st.spinner(
            "Running SOAP, symptom retrieval, triage, "
            "and escalation agents..."
        ):
            try:
                result = asyncio.run(
                    analyse_conversation(conversation)
                )

                st.success("Analysis completed.")

                st.subheader("ClinicMate Analysis")
                st.markdown(result)

            except Exception as error:
                error_message = str(error)

                if (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                ):
                    st.error(
                        "Gemini request limit reached. Please wait "
                        "for some time and try again."
                    )

                elif "medical_knowledge" in error_message:
                    st.error(
                        "The Qdrant medical knowledge collection "
                        "could not be accessed. Run qdrant_setup.py first."
                    )

                else:
                    st.error(
                        f"ClinicMate could not complete the analysis: "
                        f"{error_message}"
                    )


# ---------------------------------------------------------
# SAFETY NOTICE
# ---------------------------------------------------------

st.divider()

st.info(
    "ClinicMate supports clinical documentation and preliminary "
    "triage only. It does not replace diagnosis, treatment, or "
    "emergency care from a qualified healthcare professional."
)