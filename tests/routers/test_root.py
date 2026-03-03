import pytest


@pytest.mark.anyio
async def test_health_check(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["status"] == "ok"
