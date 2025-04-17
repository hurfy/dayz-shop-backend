# Raised when Steam authentication status cannot be parsed or validated.
class SteamCheckError(Exception):
    def __init__(self, message: str = "Failed to parse Steam authentication status") -> None:
        self.message: str = message

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


# Raised when the list of Steam players is unexpectedly empty
class EmptySteamPlayersError(Exception):
    def __init__(self, message: str = "The list of players with the specified SteamID is empty") -> None:
        self.message: str = message

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
