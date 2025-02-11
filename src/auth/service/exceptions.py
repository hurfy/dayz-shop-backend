# The response from Steam was incorrect, no validation check field or something else
class InvalidSteamResponse(Exception):
    def __init__(self, message: str):
        super().__init__(message)


# Failed to authenticate, network error or Steam is not responding
class SteamCheckError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
