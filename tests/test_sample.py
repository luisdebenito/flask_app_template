def test_health_status(test_client):
    """Check that the home page returns 200"""
    response = test_client.get("/health")
    assert response.status_code == 200
