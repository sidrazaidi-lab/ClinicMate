from google.adk.agents import Agent
from qdrant_client import QdrantClient


QDRANT_PATH = r"C:\Users\hp\my_agent\qdrant_data"
COLLECTION_NAME = "medical_knowledge"


def search_symptom(symptom: str) -> dict:
    """Search the local Qdrant medical knowledge collection."""

    # Open the client each time the tool is called
    client = QdrantClient(path=QDRANT_PATH)

    try:
        if not client.collection_exists(
            collection_name=COLLECTION_NAME
        ):
            collections = client.get_collections()

            return {
                "symptom": symptom,
                "disease": "Database collection unavailable",
                "severity": "Needs Doctor",
                "recommendation": (
                    f"Collection '{COLLECTION_NAME}' was not found. "
                    f"Available collections: {collections}"
                ),
            }

        points, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
        )

        cleaned_symptom = symptom.strip().lower()

        for point in points:
            payload = point.payload or {}
            stored_symptom = payload.get("symptom", "").strip().lower()

            if stored_symptom == cleaned_symptom:
                return payload

        return {
            "symptom": symptom,
            "disease": "Unknown",
            "severity": "Needs Doctor",
            "recommendation": (
                "The symptom was not found in the medical knowledge "
                "database. Consult a healthcare professional."
            ),
        }

    finally:
        client.close()


symptom_agent = Agent(
    model="gemini-flash-latest",
    name="symptom_agent",
    description="Extracts symptoms and retrieves medical information from Qdrant.",

    instruction="""
Read the original patient conversation and these SOAP notes:

{soap_notes}

Identify every symptom mentioned by the patient.

For each individual symptom, call the search_symptom tool.

Use simple database terms when calling the tool.

Examples:

- chest pain
- breathing difficulty
- fever
- cough
- headache

Do not call the tool with a full sentence.

Return:

Symptoms:
- symptom name

Qdrant Retrieval:
- Possible condition
- Severity
- Recommendation
""",

    tools=[search_symptom],
    output_key="symptom_results",
)