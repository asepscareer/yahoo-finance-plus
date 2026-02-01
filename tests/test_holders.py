from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_major_holders():
    response = client.post("/api/v1/major-holders", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_institutional_holders():
    response = client.post("/api/v1/institutional-holders", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_mutual_fund_holders():
    response = client.post("/api/v1/mutual-fund-holders", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_insider_roster_holders():
    response = client.post("/api/v1/insider-roster-holders", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_insider_transactions():
    response = client.post("/api/v1/insider-transactions", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_insider_purchases():
    response = client.post("/api/v1/insider-purchases", json={"symbol": "AAPL"})
    assert response.status_code == 200
