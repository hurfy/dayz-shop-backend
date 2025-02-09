from starlette                     import status
from fastapi                       import APIRouter, Depends, HTTPException
from typing                        import Annotated

from api.shared.repositories.order import OrderRepository
from api.shop.schemas.order        import OrderResponse, OrderCreate
from api.dependencies              import order_repository
from api.utils                     import HTTP_RESPONSES
from params                        import Model, Puuid

router = APIRouter(
    prefix = "/orders",
    tags   = ["Orders"],
)

repository: type[OrderRepository] = Annotated[OrderRepository, Depends(order_repository)]


# Get data -------------------------------------------------------------------------------------------------------------
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderResponse],
    description="Get a non-paginated list of orders",
)
async def read_list(repo: repository) -> list[OrderResponse]:
    """Get list of orders"""
    return await repo.read_list()


@router.get(
    path="/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Get an order by id",
)
async def read(
        repo: repository, order_id: Puuid
) -> OrderResponse:
    """Get an order by id"""
    try:
        return await repo.read(object_id=order_id)

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

# Create data ----------------------------------------------------------------------------------------------------------
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderResponse,
    description="Create a new order",
)
async def create(
        repo: repository, data: OrderCreate
) -> OrderResponse:
    """Create a new order"""
    try:
        return await repo.create(object_data=data)

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# Update data ----------------------------------------------------------------------------------------------------------
async def update_base(
        repo: OrderRepository, data: type[Model], order_id: Puuid, partial: bool = False
) -> OrderResponse:
    """update_order_base ..."""
    return await repo.update(
        object_id=order_id, object_data=data, partial=partial,
    )


@router.put(
    path="/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Update an order",
)
async def update(
        repo: repository, data: OrderCreate, order_id: Puuid
) -> OrderResponse:
    """Update an order by id"""
    try:
        return await update_base(
            repo, data, order_id, partial=False
        )

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch(
    path="/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrderResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Partial update an order",
)
async def partial_update(
        repo: repository, data: OrderCreate, order_id: Puuid
) -> OrderResponse:
    """Partial update an order by id"""
    try:
        return await update_base(
            repo, data, order_id, partial=True
        )

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# Delete data ----------------------------------------------------------------------------------------------------------
@router.delete(
    path="/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Delete an order",
)
async def delete(
        repo: repository, order_id: Puuid
) -> None:
    """Delete an order by id"""
    try:
        await repo.delete(object_id=order_id)

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
