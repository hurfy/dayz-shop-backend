# The response from Steam was incorrect, no validation check field or something else
class SteamRequestError(Exception):
    def __init__(self, status: int, message: str) -> None:
        self.status = status
        self.message = message

    def __str__(self) -> str:
        return (
            f"The request to Steam was not successful\n"
            f"Status: {self.status}\n"
            f"Message: {self.message}"
        )


# Failed to authenticate, network error or Steam is not responding
class SteamCheckError(Exception):
    def __str__(self) -> str:
        return "Authentication status parsing error"
