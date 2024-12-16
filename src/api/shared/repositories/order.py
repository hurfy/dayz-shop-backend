from uuid                   import UUID

from api.shop.schemas.order import OrderResponse
from api.shop.models.order  import EOrderStatus
from api.crud.repository    import CRUDMixin, ReadListMixin
from database               import new_session


class OrderRepository(CRUDMixin, ReadListMixin):
    async def set_status(self, object_id: UUID, status: EOrderStatus) -> OrderResponse:
        """set_status ..."""
        async with new_session() as session:
            obj = await self._get_object_or_404(
                object_id=object_id,
                session=session,
            )

            obj.status = status

            await session.commit()

            return await self._create_response(obj)

