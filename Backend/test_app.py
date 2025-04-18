import pytest
from backend.app import app, create_access_token

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_success(client):
    response = client.post("/api/login", json={"username": "admin", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_login_failure(client):
    response = client.post("/api/login", json={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401

def test_predict_requires_auth(client):
    response = client.post("/api/predict", json={})
    assert response.status_code == 401  # Unauthorized without JWT

def test_stream_fraud_requires_auth(client):
    response = client.get("/api/stream-fraud")
    assert response.status_code == 401  # Unauthorized without JWT
