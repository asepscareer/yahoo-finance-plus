from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_dividends():
    response = client.post("/api/v1/dividends", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_splits():
    response = client.post("/api/v1/splits", json={"symbol": "AAPL"})
    assert response.status_code == 200
