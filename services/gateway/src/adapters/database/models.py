from sqlalchemy.orm import DeclarativeBase
from sqlalchemy     import Column, String, UUID


class GatewayModel(DeclarativeBase):
    ...


class User(GatewayModel):
    __tablename__ = "users"

    id           : int = Column(UUID, primary_key=True)
    steam_id     : str = Column(String(17), nullable=False)
    personal_name: str = Column(String(255), nullable=False)
    profile_url  : str = Column(String(255), nullable=False)
    avatar       : str = Column(String(255), nullable=False)
    avatar_medium: str = Column(String(255), nullable=False)
    avatar_full  : str = Column(String(255), nullable=False)

    def __str__(self) -> str:
        return (
            f"Id     : {self.id}\n"
            f"SteamID: {self.steam_id}\n"
            f"Name   : {self.personal_name}\n"
            f"Profile: {self.profile_url}"
        )
