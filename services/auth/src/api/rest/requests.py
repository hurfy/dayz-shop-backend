from dzshop.enums import RoleType
from pydantic     import BaseModel, Field


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


class RefreshToken(BaseModel):
    refresh_token: str = Field(
        examples=["..."]
    )
