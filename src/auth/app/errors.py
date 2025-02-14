# Token does not contain the required field, expired or smth else
class InvalidToken(Exception):
    def __str__(self) -> str:
        return "Invalid token."
