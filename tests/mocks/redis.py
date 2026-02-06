class MockRedis:
    def __init__(self):
        self.store = {}

    def evalsha(self, sha, _, *args):
        match sha:
            case "create":
                return 1
            case "verify":
                key = args[0]
                return self.store.get(key, None)
            case "activate_token":
                key = args[0]
                if key not in self.store:
                    return 0
                return 1
            case _:
                return 3
