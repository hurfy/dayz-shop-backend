from sqlalchemy.orm import DeclarativeBase
from sqlalchemy     import Column, String, Boolean, DateTime


class AuthModel(DeclarativeBase):
    ...


class IssuedToken(AuthModel):
    __tablename__ = "issued_tokens"

    jti    : str  = Column(String(36), primary_key=True)
    revoked: bool = Column(Boolean, default=False)
    subject: str  = Column(String(17))  # just SteamId
    expired: str  = Column(DateTime)
    # device_id: str  = Column(String(36))

    def __str__(self) -> str:
        return f"{self.subject}: {self.jti}"
