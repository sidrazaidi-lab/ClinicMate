from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


# ---------------------------------------------------------
# QDRANT DATABASE PATH
# ---------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
QDRANT_PATH = PROJECT_DIR / "qdrant_data"

client = QdrantClient(path=str(QDRANT_PATH))

collection_name = "medical_knowledge"


# ---------------------------------------------------------
# DELETE OLD COLLECTION
# ---------------------------------------------------------

if client.collection_exists(collection_name=collection_name):
    client.delete_collection(collection_name=collection_name)


# ---------------------------------------------------------
# CREATE NEW COLLECTION
# ---------------------------------------------------------

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=4,
        distance=Distance.COSINE,
    ),
)


# ---------------------------------------------------------
# SAMPLE MEDICAL KNOWLEDGE
# ---------------------------------------------------------

medical_data = [
    {
        "id": 1,
        "symptom": "fever",
        "disease": "Possible viral infection or flu",
        "severity": "Needs Doctor",
        "recommendation": (
            "Rest, stay hydrated, monitor temperature, and consult "
            "a healthcare professional if the fever continues or worsens."
        ),
        "vector": [0.10, 0.20, 0.30, 0.40],
    },
    {
        "id": 2,
        "symptom": "cough",
        "disease": "Possible common cold or respiratory infection",
        "severity": "Normal",
        "recommendation": (
            "Rest, drink warm fluids, and consult a healthcare professional "
            "if the cough persists or becomes severe."
        ),
        "vector": [0.15, 0.25, 0.35, 0.45],
    },
    {
        "id": 3,
        "symptom": "headache",
        "disease": "Possible migraine, dehydration, or viral illness",
        "severity": "Needs Doctor",
        "recommendation": (
            "Rest, drink water, and consult a healthcare professional "
            "if the headache is severe or persistent."
        ),
        "vector": [0.20, 0.10, 0.40, 0.30],
    },
    {
        "id": 4,
        "symptom": "sore throat",
        "disease": "Possible throat infection or viral illness",
        "severity": "Normal",
        "recommendation": (
            "Drink warm fluids and seek medical advice if swallowing "
            "becomes difficult or symptoms worsen."
        ),
        "vector": [0.25, 0.35, 0.15, 0.45],
    },
    {
        "id": 5,
        "symptom": "runny nose",
        "disease": "Possible common cold or allergy",
        "severity": "Normal",
        "recommendation": (
            "Rest, stay hydrated, and monitor the symptoms."
        ),
        "vector": [0.30, 0.15, 0.25, 0.40],
    },
    {
        "id": 6,
        "symptom": "vomiting",
        "disease": "Possible gastroenteritis or food-related illness",
        "severity": "Needs Doctor",
        "recommendation": (
            "Take fluids in small amounts and consult a healthcare "
            "professional if vomiting continues."
        ),
        "vector": [0.35, 0.20, 0.10, 0.45],
    },
    {
        "id": 7,
        "symptom": "diarrhea",
        "disease": "Possible gastroenteritis or digestive infection",
        "severity": "Needs Doctor",
        "recommendation": (
            "Maintain hydration and seek medical advice if the condition "
            "is severe, persistent, or accompanied by weakness."
        ),
        "vector": [0.40, 0.10, 0.20, 0.30],
    },
    {
        "id": 8,
        "symptom": "stomach pain",
        "disease": "Possible indigestion, infection, or abdominal condition",
        "severity": "Needs Doctor",
        "recommendation": (
            "Consult a healthcare professional if the pain is severe, "
            "persistent, or accompanied by vomiting."
        ),
        "vector": [0.45, 0.20, 0.30, 0.10],
    },
    {
        "id": 9,
        "symptom": "dizziness",
        "disease": "Possible dehydration, low blood pressure, or other condition",
        "severity": "Needs Doctor",
        "recommendation": (
            "Sit or lie down safely and consult a healthcare professional "
            "if the dizziness continues."
        ),
        "vector": [0.30, 0.40, 0.10, 0.20],
    },
    {
        "id": 10,
        "symptom": "weakness",
        "disease": "Possible fatigue, dehydration, infection, or deficiency",
        "severity": "Needs Doctor",
        "recommendation": (
            "Rest, stay hydrated, and consult a healthcare professional "
            "if the weakness is persistent or severe."
        ),
        "vector": [0.20, 0.40, 0.30, 0.10],
    },
    {
        "id": 11,
        "symptom": "chest pain",
        "disease": "Possible cardiac or respiratory emergency",
        "severity": "Emergency",
        "recommendation": (
            "Seek immediate emergency medical care."
        ),
        "vector": [0.90, 0.10, 0.10, 0.10],
    },
    {
        "id": 12,
        "symptom": "breathing difficulty",
        "disease": "Possible respiratory emergency",
        "severity": "Emergency",
        "recommendation": (
            "Seek immediate emergency medical care."
        ),
        "vector": [0.85, 0.15, 0.10, 0.10],
    },
    {
        "id": 13,
        "symptom": "shortness of breath",
        "disease": "Possible respiratory or cardiac emergency",
        "severity": "Emergency",
        "recommendation": (
            "Seek immediate emergency medical care."
        ),
        "vector": [0.80, 0.20, 0.10, 0.10],
    },
    {
        "id": 14,
        "symptom": "severe bleeding",
        "disease": "Possible major blood loss or injury",
        "severity": "Emergency",
        "recommendation": (
            "Apply direct pressure if it is safe to do so and seek "
            "emergency medical assistance immediately."
        ),
        "vector": [0.95, 0.05, 0.05, 0.05],
    },
    {
        "id": 15,
        "symptom": "confusion",
        "disease": "Possible neurological, metabolic, or medical emergency",
        "severity": "Emergency",
        "recommendation": (
            "Seek immediate professional medical care."
        ),
        "vector": [0.75, 0.10, 0.10, 0.25],
    },
    {
        "id": 16,
        "symptom": "fainting",
        "disease": "Possible cardiac, circulatory, or neurological condition",
        "severity": "Emergency",
        "recommendation": (
            "Seek immediate medical assistance."
        ),
        "vector": [0.70, 0.20, 0.05, 0.25],
    },
]


# ---------------------------------------------------------
# CONVERT DATA INTO QDRANT POINTS
# ---------------------------------------------------------

points = []

for item in medical_data:
    points.append(
        PointStruct(
            id=item["id"],
            vector=item["vector"],
            payload={
                "symptom": item["symptom"],
                "disease": item["disease"],
                "severity": item["severity"],
                "recommendation": item["recommendation"],
            },
        )
    )


# ---------------------------------------------------------
# INSERT POINTS INTO QDRANT
# ---------------------------------------------------------

client.upsert(
    collection_name=collection_name,
    points=points,
    wait=True,
)


# ---------------------------------------------------------
# VERIFY COLLECTION
# ---------------------------------------------------------

stored_points, _ = client.scroll(
    collection_name=collection_name,
    limit=100,
)

print("Qdrant setup completed successfully.")
print(f"{len(stored_points)} medical symptom records added.")
print(f"Database location: {QDRANT_PATH}")
print(f"Collection name: {collection_name}")

client.close()