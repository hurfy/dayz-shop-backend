from fastapi                         import APIRouter, status

from api.shared.repositories.product import ProductRepository
from api.shop.schemas.product        import ProductResponse, ProductCreate, ProductUpdate
from api.utils                       import HTTP_RESPONSES
from params                          import Model, uuid_

router = APIRouter(
    prefix = "/products",
    tags   = ["Products"],
)


# Get data -------------------------------------------------------------------------------------------------------------
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProductResponse],
)
async def get_list() -> list[ProductResponse]:
    """Get list of products"""
    return await ProductRepository.fetch_list()


@router.get(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    responses={
            404: HTTP_RESPONSES[404],
    },
)
async def get(product_id: uuid_) -> ProductResponse:
    """Get product by id"""
    return await ProductRepository.fetch(
        object_id=product_id
    )


# Create data ----------------------------------------------------------------------------------------------------------
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse,
)
async def create(product_data: ProductCreate) -> ProductResponse:
    """Create a product"""
    return await ProductRepository.create(object_data=product_data)


# Update data ----------------------------------------------------------------------------------------------------------
async def update_base(
        product_data: type[Model], product_id: uuid_, partial: bool = False
) -> ProductResponse:
    """update_product_base ..."""
    return await ProductRepository.update(
        object_id=product_id,
        object_data=product_data,
        partial=partial,
    )

@router.put(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def update(product_data: ProductCreate, product_id: uuid_) -> ProductResponse:
    """Update the product"""
    return await update_base(product_data, product_id, partial=False)


@router.patch(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def partial_update(product_data: ProductUpdate, product_id: uuid_) -> ProductResponse:
    """Partial update the product"""
    return await update_base(product_data, product_id, partial=True)


# Delete data ----------------------------------------------------------------------------------------------------------
@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def delete(product_id: uuid_) -> None:
    """Delete the product"""
    await ProductRepository.delete(product_id)
