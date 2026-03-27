from typing import Any, AsyncGenerator

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health_check(client: AsyncGenerator[AsyncClient, Any]) -> None:
    response = await client.head("/")
    assert response.status_code == 200
