import os
os.environ["DATABASE_URL"] = "sqlite:///./test_analytics.db"
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_event_and_summary():
    r = client.post("/events", json={"user_id":"u1","event_type":"purchase","value":25.5})
    assert r.status_code == 201
    data = client.get("/analytics/summary").json()
    assert data["total_events"] >= 1
    assert data["total_value"] >= 25.5
