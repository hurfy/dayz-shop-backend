class UserWriteError(Exception):
    def __init__(self, action: str, original: Exception):
        super().__init__(f"Failed to {action} user: {original}")
        self.original: Exception = original
