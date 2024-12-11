from sqlalchemy             import select
from fastapi                import HTTPException
from uuid                   import UUID

from api.shop.schemas.order import OrderSchema, OrderResponse
from api.shop.models.order  import MOrder, EOrderStatus
from api.crud.repository    import CRUDMixin, GetListMixin
from database               import new_session


class OrderRepository(CRUDMixin, GetListMixin):
    model  = MOrder
    schema = OrderSchema

    @classmethod
    async def set_status(cls, object_id: UUID, status: EOrderStatus) -> OrderResponse:
        """set_status ..."""
        async with new_session() as session:
            order = await session.execute(
                select(MOrder).filter(MOrder.id == object_id)
            )

            if not (obj := order.scalar_one_or_none()):
                raise HTTPException(
                    status_code=404,
                    detail=f"category with id {object_id} not found"
                )

            obj.status = status

            await session.commit()

            return await cls.response_data(obj)

