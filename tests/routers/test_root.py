import pytest


@pytest.mark.anyio
async def test_health_check(client):
    response = await client.head("/")
    assert response.status_code == 200
