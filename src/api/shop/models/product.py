import enum
import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy     import Enum, ForeignKey

from database       import Model


class ProductType(str, enum.Enum):
    PURCHASE = "purchase"
    SELL     = "sell"


class MProduct(Model):
    __tablename__  = "shop_products"

    id               : Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name             : Mapped[str]
    category_id      : Mapped[int] = mapped_column(ForeignKey("shop_categories.id"))
    surcharge        : Mapped[int] = mapped_column(default=0)
    original_price   : Mapped[int]
    type             : Mapped[ProductType] = mapped_column(Enum(ProductType))
    count            : Mapped[int]
    description      : Mapped[str | None]
    image_url        : Mapped[str]
    is_discount_apply: Mapped[bool]
    is_show          : Mapped[bool]
