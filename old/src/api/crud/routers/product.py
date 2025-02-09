from fastapi                         import APIRouter, Depends, HTTPException, status
from typing                          import Annotated

from api.shared.repositories.product import ProductRepository
from api.shop.schemas.product        import ProductResponse, ProductCreate, ProductUpdate
from api.dependencies                import product_repository
from api.utils                       import HTTP_RESPONSES
from params                          import Model, Puuid

router = APIRouter(
    prefix = "/products",
    tags   = ["Products"],
)

repository: type[ProductRepository] = Annotated[ProductRepository, Depends(product_repository)]


# Get data -------------------------------------------------------------------------------------------------------------
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProductResponse],
    description="Get a non-paginated list of products",
)
async def read_list(repo: repository) -> list[ProductResponse]:
    """Get list of products"""
    return await repo.read_list()


@router.get(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    responses={
            404: HTTP_RESPONSES[404],
    },
    description="Get a product by id",
)
async def read(
        repo: repository, product_id: Puuid
) -> ProductResponse:
    """Get a product by id"""
    try:
        return await repo.read(object_id=product_id)

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# Create data ----------------------------------------------------------------------------------------------------------
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse,
    description="Create new product",
)
async def create(
        repo: repository, product_data: ProductCreate
) -> ProductResponse:
    """Create new product"""
    try:
        return await repo.create(object_data=product_data)

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

# Update data ----------------------------------------------------------------------------------------------------------
async def update_base(
        repo: ProductRepository, product_data: type[Model], product_id: Puuid, partial: bool = False
) -> ProductResponse:
    """update_product_base ..."""
    return await repo.update(
        object_id=product_id, object_data=product_data, partial=partial,
    )

@router.put(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Update a product",
)
async def update(
        repo: repository, product_data: ProductCreate, product_id: Puuid
) -> ProductResponse:
    """Update a product by id"""
    try:
        return await update_base(
            repo, product_data, product_id, partial=False
        )

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Partial update a product",
)
async def partial_update(
        repo: repository, product_data: ProductUpdate, product_id: Puuid
) -> ProductResponse:
    """Partial update a product by id"""
    try:
        return await update_base(
            repo, product_data, product_id, partial=True
        )

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# Delete data ----------------------------------------------------------------------------------------------------------
@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Delete a product",
)
async def delete(
        repo: repository, product_id: Puuid
) -> None:
    """Delete a product by id"""
    try:
        await repo.delete(product_id)

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
