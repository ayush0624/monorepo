import pytest
from fastapi.testclient import TestClient
from projects.concord.app.api import app

@pytest.fixture(scope="function")
def client():
    """Create a test client"""
    with TestClient(app) as c:
        yield c

class TestPingEndpoint:
    """Tests for the /ping endpoint."""

    def test_ping_returns_pong(self, client):
        """Test that ping endpoint returns correct response."""
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}
