from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_generate():

    payload = {
        "document_type": "Freelance Work Contract",
        "parties": "Jane Doe; TechNova Inc.",
        "terms": (
            "Payment within 7 days; "
            "Confidentiality applies."
        ),
        "effective_date": "2025-04-15",
        "jurisdiction": "Not specified",
        "additional_instructions": (
            "Use professional language."
        ),
    }

    response = client.post(
        "/api/generate",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["content"]
    assert (
        data["document_type"]
        == "Freelance Work Contract"
    )