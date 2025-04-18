from enum import Enum


class RoleType(str, Enum):
    admin: str = "admin"
    user : str = "user"
