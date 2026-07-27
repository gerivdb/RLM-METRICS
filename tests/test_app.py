import pytest
from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["service"] == "rlm-metrics"


def test_metrics(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "phi_cps" in data
    assert "benchmarks" in data
    assert "health" in data


def test_vote_success(client):
    resp = client.post("/vote", json={"choice": "yes"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["choice"] == "yes"


def test_vote_missing_choice(client):
    resp = client.post("/vote", json={})
    assert resp.status_code == 400


def test_collect_success(client):
    resp = client.post("/collect", json={"source": "rlm-config", "metric": "phi_cps", "value": 3.697})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["accepted"] is True


def test_collect_missing_fields(client):
    resp = client.post("/collect", json={"source": "rlm-config"})
    assert resp.status_code == 400


def test_status(client):
    resp = client.get("/status")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["service"] == "rlm-metrics"
