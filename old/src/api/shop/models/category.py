from sqlalchemy.orm import Mapped, mapped_column

from database       import Model


class MCategory(Model):
    __tablename__ = "shop_categories"

    id         : Mapped[int] = mapped_column(primary_key=True)
    name       : Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    is_show    : Mapped[bool]
