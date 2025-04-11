from pydantic     import BaseModel, Field

from dzshop.enums import RoleType


class TokenPair(BaseModel):
    access_token : str
    refresh_token: str
    token_type   : str = "Bearer"


class CreateToken(BaseModel):
    steam_id: str = Field(
        max_length=17,
        min_length=17,
        pattern=r"^\d+$",
        examples=["76561198181797231"]
    )
    role: RoleType = Field(
        default=RoleType.user,
        examples=[RoleType.user, RoleType.admin]
    )
