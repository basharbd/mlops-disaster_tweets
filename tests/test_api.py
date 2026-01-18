from fastapi.testclient import TestClient

from disaster_tweets.api import app

# Create a test client that wraps your real app
client = TestClient(app)


def test_read_root():
    """Test that the root endpoint returns the correct welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    # Update this line to match your actual API message:
    assert response.json() == {"message": "Disaster Tweet Classifier is Ready!"}


def test_predict_disaster():
    """Test a clear disaster tweet."""
    response = client.post(
        "/predict", json={"text": "Huge fire in the forest! Everyone is running."}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "prediction" in json_data
    assert "class_id" in json_data
    # We expect this to be classified as a disaster (but we check structure mostly)
    assert isinstance(json_data["prediction"], str)


def test_predict_safe():
    """Test a clear non-disaster tweet."""
    response = client.post(
        "/predict", json={"text": "I love looking at the blue sky today."}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "prediction" in json_data
    # Usually this is "Not Disaster", but models vary. We verify it didn't crash.
    assert response.status_code == 200


def test_predict_empty_input():
    """Test what happens if we send invalid data (empty JSON)."""
    response = client.post(
        "/predict",
        json={},  # Missing "text" field
    )
    # FastAPI should automatically block this with a 422 Unprocessable Entity error
    assert response.status_code == 422
