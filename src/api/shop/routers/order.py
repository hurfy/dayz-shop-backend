from fastapi                       import APIRouter, status

from api.shared.repositories.order import OrderRepository
from api.shop.schemas.order        import OrderResponse, OrderStatus
from api.utils                     import HTTP_RESPONSES
from params                        import uuid_

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

@router.patch(
    path="/{order_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def set_status(order_id: uuid_, new_status: OrderStatus) -> OrderResponse:
    """change_order_status ..."""
    return await OrderRepository.set_status(object_id=order_id, status=new_status.status)

# completed canceled
@router.patch(
    path="/{order_id}/status/complete",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def complete(order_id: uuid_) -> OrderResponse:
    """complete ..."""
    return await OrderRepository.set_status(object_id=order_id, status="completed")


@router.patch(
    path="/{order_id}/status/cancel",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def cancel(order_id: uuid_) -> OrderResponse:
    """cancel ..."""
    return await OrderRepository.set_status(object_id=order_id, status="canceled")
