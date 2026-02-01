from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_financials():
    response = client.post("/api/v1/financials", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_quarterly_financials():
    response = client.post("/api/v1/quarterly-financials", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_income_stmt():
    response = client.post("/api/v1/income-statement", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_quarterly_income_stmt():
    response = client.post("/api/v1/quarterly-income-statement", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_balance_sheet():
    response = client.post("/api/v1/balance-sheet", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_quarterly_balance_sheet():
    response = client.post("/api/v1/quarterly-balance-sheet", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_cash_flow():
    response = client.post("/api/v1/cash-flow", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_quarterly_cash_flow():
    response = client.post("/api/v1/quarterly-cash-flow", json={"symbol": "AAPL"})
    assert response.status_code == 200
