from sqlalchemy.orm import DeclarativeBase
from sqlalchemy     import Column, String, Boolean, DateTime, Enum

from core.enums     import TokenType


class AuthModel(DeclarativeBase):
    ...


class IssuedToken(AuthModel):
    __tablename__ = "issued_tokens"

    jti    : str  = Column(String(36), primary_key=True)
    revoked: bool = Column(Boolean, default=False, nullable=False)
    subject: str  = Column(String(17), nullable=False)  # just SteamId
    expired: str  = Column(DateTime, nullable=False)
    type   : str  = Column(Enum(TokenType), nullable=False)
    # device_id: str  = Column(String(36))

    def __str__(self) -> str:
        return f"{self.subject}: {self.jti}"
