import os
import time
import pytest
import unittest
from fastapi.testclient import TestClient
from main import app

# Create a TestClient instance for the app.
client = TestClient(app)


# Fixture to ensure the CPU stress test feature is enabled for tests.
@pytest.fixture(autouse=True)
def set_stress_flag(monkeypatch):
    monkeypatch.setenv("STRESS_TEST_FLAG", "true")
    yield
    monkeypatch.delenv("STRESS_TEST_FLAG", raising=False)


def test_home_page():
    """Test that the home page returns a 200 response and contains the app name."""
    response = client.get("/")
    assert response.status_code == 200
    # Verify the title or header is present.
    assert "Devops Leaders IL Course - Test App" in response.text


def test_weather_endpoint(monkeypatch):
    """Test the /weather endpoint by monkeypatching requests.get."""

    class DummyResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json = json_data

        def json(self):
            return self._json

    def dummy_get(url):
        dummy_data = {
            "current_condition": [
                {"temp_C": "20", "weatherDesc": [{"value": "Sunny"}]}
            ],
            "nearest_area": [
                {
                    "areaName": [{"value": "TestCity"}],
                    "latitude": "40.0",
                    "longitude": "-74.0",
                }
            ],
        }
        return DummyResponse(200, dummy_data)

    monkeypatch.setattr("requests.get", dummy_get)

    response = client.get("/weather?location=TestCity")
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "TestCity"
    assert data["temperature"] == "20"
    assert "Sunny" in data["description"]
