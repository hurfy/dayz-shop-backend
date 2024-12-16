from fastapi                       import APIRouter, Depends, HTTPException, status
from typing                        import Annotated

from api.shared.repositories.order import OrderRepository
from api.shop.schemas.order        import OrderResponse, OrderStatus
from api.dependencies              import order_repository
from api.utils                     import HTTP_RESPONSES
from params                        import Puuid

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

repository: type[OrderRepository] = Annotated[OrderRepository, Depends(order_repository)]


@router.patch(
    path="/{order_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Set the order status to the specified",
)
async def set_status(
        repo: repository, order_id: Puuid, new_status: OrderStatus
) -> OrderResponse:
    """Set the order status to the specified"""
    try:
        return await repo.set_status(
            object_id=order_id, status=new_status.status
        )

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch(
    path="/{order_id}/status/complete",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Mark an order as completed",
)
async def complete(
        repo: repository, order_id: Puuid
) -> OrderResponse:
    """Mark an order as completed"""
    try:
        return await repo.set_status(
            object_id=order_id, status="completed"
        )

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch(
    path="/{order_id}/status/cancel",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Mark an order as canceled",
)
async def cancel(
        repo: repository, order_id: Puuid
) -> OrderResponse:
    """Mark an order as canceled"""
    try:
        return await repo.set_status(
            object_id=order_id, status="canceled"
        )

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
