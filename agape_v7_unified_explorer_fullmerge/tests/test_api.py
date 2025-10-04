from fastapi.testclient import TestClient
from hub.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True

def test_state_roundtrip():
    r = client.get("/state/get")
    assert r.status_code == 200
    s = r.json()
    # update a j-metric
    r2 = client.post("/state/update", json={"jMetrics":{"j1": 0.7}})
    assert r2.status_code == 200
    s2 = r2.json()
    assert abs(s2["jMetrics"]["j1"] - 0.7) < 1e-9
