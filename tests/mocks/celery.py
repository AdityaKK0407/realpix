class MockCelery:
    def __init__(self, task_id):
        self.id = task_id


class MockCeleryAsyncResult:
    def __init__(self, state, result):
        self.state = state
        self.result = result
