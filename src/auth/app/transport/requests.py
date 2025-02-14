from pydantic import BaseModel
from typing   import Literal


class Create(BaseModel):
    steam_id: str
    role    : Literal["user", "admin"] = "user"


class Refresh(BaseModel):
    refresh_token: str
