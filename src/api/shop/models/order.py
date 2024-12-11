import enum
import uuid

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm                 import Mapped, mapped_column
from sqlalchemy                     import Enum, JSON

from database                       import Model


class EOrderStatus(str, enum.Enum):
    WAITING   = "waiting"
    COMPLETED = "completed"
    CANCELED  = "canceled"


class MOrder(Model):
    __tablename__ = "shop_orders"

    id      : Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    status  : Mapped[EOrderStatus] = mapped_column(Enum(EOrderStatus))
    user_id : Mapped[uuid.UUID]  # must be relationship
    total   : Mapped[int] = mapped_column(nullable=False)
    products: Mapped[JSON] = mapped_column(JSONB)
