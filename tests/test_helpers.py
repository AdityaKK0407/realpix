from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from src.helpers import load_lua_script


@pytest.mark.anyio
async def test_load_lua_script(tmp_path: Path) -> None:
    lua_content = "lua script"
    lua_file = tmp_path / "lua.lua"
    lua_file.write_text(lua_content)

    mock_redis = AsyncMock()
    mock_redis.script_load.return_value = "fake_sha"

    sha = await load_lua_script(mock_redis, str(lua_file))

    assert sha == "fake_sha"
    mock_redis.script_load.assert_awaited_once_with(lua_content)
