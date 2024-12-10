import enum
import uuid

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm                 import Mapped, mapped_column
from sqlalchemy                     import Enum, JSON

from database                       import Model


class OrderStatus(str, enum.Enum):
    WAITING   = "waiting"
    COMPLETED = "completed"
    CANCELED  = "canceled"


class MOrder(Model):
    __tablename__ = "shop_orders"

    id      : Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    status  : Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))
    user_id : Mapped[uuid.UUID]  # must be relationship
    total   : Mapped[int] = mapped_column(nullable=False)
    products: Mapped[JSON] = mapped_column(JSONB)
