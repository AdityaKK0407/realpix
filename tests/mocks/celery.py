class MockCelery:
    def __init__(self, task_id: str) -> None:
        self.id = task_id


class MockCeleryAsyncResult:
    def __init__(self, state: str | None, result: list[bool]) -> None:
        self.state = state
        self.result = result
