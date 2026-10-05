from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Welcome Portal" in response.text


def test_api_welcome_overview():
    response = client.get("/api/welcome")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "title" in data


def test_create_welcome_greeting():
    payload = {
        "name": "David Miller",
        "role": "Lead Architect",
        "style": "futuristic",
    }
    response = client.post("/api/welcome", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "DAVID MILLER" in data["message"]
    assert "Lead Architect" in data["personalized_note"]
    assert data["visitor"]["name"] == "David Miller"


def test_visitors_and_health():
    v_res = client.get("/api/visitors")
    assert v_res.status_code == 200
    assert len(v_res.json()) >= 1

    h_res = client.get("/api/health")
    assert h_res.status_code == 200
    assert h_res.json()["status"] == "healthy"
