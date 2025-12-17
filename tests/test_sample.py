import pytest
from main import app


@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_status(test_client):
    """Check that the home page returns 200"""
    response = test_client.get("/health")
    assert response.status_code == 200
