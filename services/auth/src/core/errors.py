# Raised when a token is invalid, missing required fields, or expired
class InvalidToken(Exception):
    def __init__(self, message: str = "Invalid token.") -> None:
        self.message: str = message

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
