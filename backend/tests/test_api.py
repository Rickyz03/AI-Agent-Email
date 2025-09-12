from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Agent Email" in response.json()["message"]


def test_draft_endpoint():
    payload = {
        "subject": "Test subject",
        "body": "This is a test email body",
        "from_addr": "sender@example.com",
        "to_addrs": ["receiver@example.com"]
    }
    response = client.post("/draft", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "variants" in data
    assert isinstance(data["variants"], list)
    assert "intent" in data
    assert "priority" in data
    assert "summary" in data
