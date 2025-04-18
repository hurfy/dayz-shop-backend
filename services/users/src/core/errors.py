# Raised when there is an error while attempting to create or write user data
class UserWriteError(Exception):
    def __init__(self, action: str, message: str = "Failed to write user data.") -> None:
        self.action : str = action
        self.message: str = f"{message} Action: {action}"

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
