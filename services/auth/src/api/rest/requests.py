from pydantic import BaseModel, Field


class RefreshTokenDTO(BaseModel):
    refresh_token: str = Field(
        examples=["..."]
    )
