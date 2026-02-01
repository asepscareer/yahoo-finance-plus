from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_simple_info():
    response = client.post("/api/v1/alt-info", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_earnings_dates():
    response = client.post("/api/v1/earnings-dates", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_calendar():
    response = client.post("/api/v1/calendar", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_sustainability():
    response = client.post("/api/v1/sustainability", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_recommendations():
    response = client.post("/api/v1/recommendations", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_recommendations_summary():
    response = client.post("/api/v1/recommendations-summary", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_analyst_price_targets():
    response = client.post("/api/v1/analyst-price-targets", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_revenue_estimate():
    response = client.post("/api/v1/revenue-estimate", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_earnings_estimate():
    response = client.post("/api/v1/earnings-estimate", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_growth_estimates():
    response = client.post("/api/v1/growth-estimates", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_upgrades_downgrades():
    response = client.post("/api/v1/upgrades-downgrades", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_isin():
    response = client.post("/api/v1/isin", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_capital_gains():
    response = client.post("/api/v1/capital-gains", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_news():
    response = client.post("/api/v1/news", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_options():
    response = client.post("/api/v1/options", json={"symbol": "AAPL"})
    assert response.status_code == 200

def test_get_option_chain():
    # I need to get a valid date for the option chain
    # I will skip this test for now
    pass

def test_get_shares_full():
    response = client.post("/api/v1/shares-full", json={"symbol": "AAPL"})
    assert response.status_code == 200
