from sqlalchemy              import Column, String, Boolean

from dzshop.modules.database import Model


class IssuedToken(Model):
    __tablename__ = "issued_tokens"

    jti    : str  = Column(String(36), primary_key=True)
    revoked: bool = Column(Boolean, default=False)
    subject: str  = Column(String(17))  # just SteamId
    # device_id: str  = Column(String(36))

    def __str__(self) -> str:
        return f"{self.subject}: {self.jti}"
