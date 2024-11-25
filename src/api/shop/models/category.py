from sqlalchemy.orm            import Mapped, mapped_column
from typing                    import Optional

from core.database import Model


class MCategory(Model):
    __tablename__ = "shop_categories"

    id         : Mapped[int] = mapped_column(primary_key=True)
    name       : Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    is_show    : Mapped[bool]