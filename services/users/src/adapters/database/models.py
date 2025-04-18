from sqlalchemy.orm import DeclarativeBase
from sqlalchemy     import Column, String, UUID
from uuid           import uuid4


class UsersModel(DeclarativeBase):
    ...


class User(UsersModel):
    __tablename__ = "users"

    id           : UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    steam_id     : str = Column(String(17), nullable=False)
    persona_name : str = Column(String(255), nullable=False)
    profile_url  : str = Column(String(255), nullable=False)
    avatar_medium: str = Column(String(255), nullable=False)
    avatar_full  : str = Column(String(255), nullable=False)

    def __str__(self) -> str:
        return (
            f"Id     : {self.id}\n"
            f"SteamID: {self.steam_id}\n"
            f"Name   : {self.persona_name}\n"
            f"Profile: {self.profile_url}"
        )
