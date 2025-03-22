import pytest
from portfolio import app

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_app_running(client):
    """Test to ensure the app is running and responds to a request."""
    response = client.get('/')
    assert response.status_code in (200, 404), "App should respond with 200 or 404 status code"
