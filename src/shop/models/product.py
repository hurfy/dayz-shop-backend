from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm                 import Mapped, mapped_column
from typing                         import Optional
from uuid                           import uuid4

from database                       import Model


class MProduct(Model):
    __tablename__ = "shop_products"

    id             : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    name           : Mapped[str]
    purchase_price : Mapped[int]
    selling_price  : Mapped[int]
    count          : Mapped[int]
    description    : Mapped[Optional[str]]
    category_id    : Mapped[int]
    image_url      : Mapped[str]
    is_show        : Mapped[bool]
