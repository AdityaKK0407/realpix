from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_home_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}
