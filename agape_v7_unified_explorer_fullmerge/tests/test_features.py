
from fastapi.testclient import TestClient
from hub.app import app

client = TestClient(app)

def test_pdf_export():
    r = client.get("/export/pdf")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/pdf")

def test_learning_endpoints():
    r = client.post("/learning/j4/infonce", json={"gain": 0.1})
    assert r.status_code == 200
    r = client.post("/learning/j5/fit", json={"target": 0.1})
    assert r.status_code == 200

def test_sde_step():
    r = client.post("/sim/hamiltonian/step", json={"angle": 0.2})
    assert r.status_code == 200
