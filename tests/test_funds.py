from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_funds_data():
    response = client.post("/api/v1/funds-data", json={"symbol": "VTSAX"})
    assert response.status_code == 200
