from typing import Any


class MockRedis:
    def __init__(self) -> None:
        self.store: dict[str, int] = {}

    def evalsha(self, sha: str, _: Any, *args) -> int | None:
        match sha:
            case "create":
                return 1
            case "verify":
                key: str = args[0]
                return self.store.get(key, None)
            case "activate_token":
                key = args[0]
                if key not in self.store:
                    return 0
                return 1
            case "ip_rate_limiter":
                return 1
            case _:
                return 3
