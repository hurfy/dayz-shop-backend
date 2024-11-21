from sqlalchemy.orm import Mapped, mapped_column
from typing         import Optional

from database       import Model


class MProduct(Model):
    __tablename__ = "shop_products"

    id             : Mapped[int] = mapped_column(primary_key=True)
    name           : Mapped[str]
    purchase_price : Mapped[int]
    selling_price  : Mapped[int]
    count          : Mapped[int]
    description    : Mapped[Optional[str]]
    category_id    : Mapped[int]
    image_url      : Mapped[str]
    is_show        : Mapped[bool]