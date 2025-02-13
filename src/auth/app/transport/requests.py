from pydantic import BaseModel


class Refresh(BaseModel):
    refresh_token: str
