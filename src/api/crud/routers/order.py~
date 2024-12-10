from starlette             import status
from fastapi               import APIRouter

from api.crud.repositories import OrderRepository
from api.shop.schemas      import OrderResponse, OrderCreate
from api.utils             import HTTP_RESPONSES
from params                import Model, uuid_

router = APIRouter(
    prefix = "/orders",
    tags   = ["Orders"],
)


# Get data -------------------------------------------------------------------------------------------------------------
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderResponse],
)
async def get_orders_list() -> list[OrderResponse]:
    """Get list of orders"""
    return await OrderRepository.fetch_list()


@router.get(
    path="/{order_id}",
    status_code=status.HTTP_200_OK,
    # response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def get_order(order_id: uuid_) -> OrderResponse:
    """Get order by id"""
    return await OrderRepository.fetch(
        object_id=order_id
    )


# Create data ----------------------------------------------------------------------------------------------------------
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderResponse,
)
async def create_order(order_data: OrderCreate) -> OrderResponse:
    """Create a product"""
    return await OrderRepository.create(object_data=order_data)


# Update data ----------------------------------------------------------------------------------------------------------
async def update_order_base(
        order_data: type[Model], order_id: uuid_, partial: bool = False
) -> OrderResponse:
    """..."""
    return await OrderRepository.update(
        object_id=order_id,
        object_data=order_data,
        partial=partial,
    )


@router.put(
    path="/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def update_order(order_data: OrderCreate, order_id: uuid_) -> OrderResponse:
    """Update the order"""
    return await update_order_base(order_data, order_id, partial=False)


@router.patch(
    path="/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def partial_update_order(order_data: OrderCreate, order_id: uuid_) -> OrderResponse:
    """Partial update the order"""
    return await update_order_base(order_data, order_id, partial=True)


# Delete data ----------------------------------------------------------------------------------------------------------
@router.delete(
    path="/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def delete_order(order_id: uuid_) -> None:
    """Delete the order"""
    await OrderRepository.delete(
        object_id=order_id
    )
