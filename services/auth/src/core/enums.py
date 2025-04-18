from enum import Enum


class TokenType(str, Enum):
    access : str = "access"
    refresh: str = "refresh"
