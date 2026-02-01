from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_stock_info():
    response = client.post("/api/v1/info", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_price():
    response = client.post("/api/v1/price", json={"symbol": "AAPL", "period": "1mo", "interval": "1d"})
    assert response.status_code == 200

def test_price_max_history():
    response = client.post("/api/v1/price-max-history", json={"symbol": "AAPL", "interval": "1d", "start": 1, "limit": 10})
    assert response.status_code == 200
