from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_price_custom_date():
    response = client.post("/api/v1/price-custom-date", json={"symbol": "AAPL", "start": "01-01-2026", "end": "31-01-2026"})
    assert response.status_code == 200
