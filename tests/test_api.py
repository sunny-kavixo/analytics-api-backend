import os
from pathlib import Path
from tempfile import TemporaryDirectory

TEST_DATABASE_DIRECTORY=TemporaryDirectory()
TEST_DATABASE_PATH=Path(TEST_DATABASE_DIRECTORY.name)/"test_analytics.db"
os.environ["DATABASE_URL"]=f"sqlite:///{TEST_DATABASE_PATH}"
import pytest
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get("/health").json()=={"status":"ok"}
def test_event_and_summary():
    r=client.post("/events",json={"user_id":"u1","event_type":"purchase","value":25.5})
    assert r.status_code==201
    d=client.get("/analytics/summary").json()
    assert d["total_events"]>=1 and d["total_value"]>=25.5

@pytest.mark.parametrize("field", ["user_id", "event_type"])
@pytest.mark.parametrize("value", ["   ", "\t", "\n", " \t\n "])
def test_whitespace_only_identifiers_are_rejected(field, value):
    payload={"user_id":"u1","event_type":"purchase","value":1}
    payload[field]=value
    before=client.get("/analytics/summary").json()["total_events"]

    response=client.post("/events",json=payload)

    assert response.status_code==422
    after=client.get("/analytics/summary").json()["total_events"]
    assert after==before

def test_identifier_whitespace_is_trimmed_and_persisted():
    response=client.post("/events",json={
        "user_id":"  user-42\t",
        "event_type":"\n purchase  ",
        "value":10,
    })

    assert response.status_code==201
    created=response.json()
    assert created["user_id"]=="user-42"
    assert created["event_type"]=="purchase"

    events=client.get("/events",params={"limit":500}).json()
    persisted=next(event for event in events if event["id"]==created["id"])
    assert persisted["user_id"]=="user-42"
    assert persisted["event_type"]=="purchase"

def test_valid_identifiers_remain_unchanged():
    response=client.post("/events",json={
        "user_id":"user_123",
        "event_type":"model.evaluation-completed",
        "value":5,
    })

    assert response.status_code==201
    assert response.json()["user_id"]=="user_123"
    assert response.json()["event_type"]=="model.evaluation-completed"

def test_normalized_identifier_length_boundary():
    boundary="x"*100
    response=client.post("/events",json={
        "user_id":f" {boundary} ",
        "event_type":boundary,
        "value":0,
    })

    assert response.status_code==201
    assert response.json()["user_id"]==boundary
    assert response.json()["event_type"]==boundary

@pytest.mark.parametrize("field", ["user_id", "event_type"])
def test_identifiers_longer_than_limit_are_rejected(field):
    payload={"user_id":"u1","event_type":"purchase","value":0}
    payload[field]="x"*101

    response=client.post("/events",json=payload)

    assert response.status_code==422
