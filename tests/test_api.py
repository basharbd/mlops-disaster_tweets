import sys
from pathlib import Path

# Fail-safe path injection
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest
from fastapi.testclient import TestClient
from disaster_tweets.api import app

# Create a test client that wraps your real app
client = TestClient(app)

def test_read_root():
    """Test that the root endpoint returns 200 (either JSON or HTML)."""
    response = client.get("/")
    assert response.status_code == 200
    # If using StaticFiles, it returns HTML. If using a JSON endpoint, check JSON.
    # For now, we just ensure the server is alive.

def test_predict_disaster():
    """Test a clear disaster tweet."""
    response = client.post(
        "/predict", json={"text": "Huge fire in the forest! Everyone is running."}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "prediction" in json_data
    assert isinstance(json_data["prediction"], str)

def test_predict_safe():
    """Test a clear non-disaster tweet."""
    response = client.post(
        "/predict", json={"text": "I love looking at the blue sky today."}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "prediction" in json_data

def test_predict_empty_input():
    """Test what happens if we send invalid data (missing 'text' field)."""
    response = client.post(
        "/predict",
        json={},  # Missing "text" field
    )
    # FastAPI automatically blocks this with a 422 Unprocessable Entity error
    assert response.status_code == 422
