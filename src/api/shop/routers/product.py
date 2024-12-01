from fastapi               import APIRouter, HTTPException, status
from typing                import List, Type

from api.shop.repositories import ProductRepository
from api.shop.schemas      import ProductResponse, ProductCreate, ProductUpdate
from api.utils             import HTTP_RESPONSES
from schemas               import Model, uuid_

router = APIRouter(
    prefix = "/products",
    tags   = ["Products"],
)



# Get data -------------------------------------------------------------------------------------------------------------
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[ProductResponse],
)
async def get_product_list() -> list[ProductResponse]:
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
async def get_product(product_id: str = uuid_) -> ProductResponse:
    """Get product by ID"""
    try:
        return await ProductRepository.fetch(
            object_id=product_id
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Create data ----------------------------------------------------------------------------------------------------------
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse,
)
async def create_product(product_data: ProductCreate) -> ProductResponse:
    """Create a product"""
    # return await ProductRepository.create_product(product_data)
    return await ProductRepository.create(
        object_data=product_data,
    )


# Update data ----------------------------------------------------------------------------------------------------------
async def update_product_base(
        product_data: Type[Model], product_id: str = uuid_, partial: bool = False
) -> ProductResponse:
    try:
        return await ProductRepository.update(
            object_id=product_id,
            object_data=product_data,
            partial=partial
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def update_product(product_data: ProductCreate, product_id: str = uuid_) -> ProductResponse:
    """Update the product"""
    return await update_product_base(product_data, product_id, partial=False)


@router.patch(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def partial_update_product(product_data: ProductUpdate, product_id: str = uuid_) -> ProductResponse:
    """Partial update the product"""
    return await update_product_base(product_data, product_id, partial=True)


# Delete data ----------------------------------------------------------------------------------------------------------
@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def delete_product(product_id: str = uuid_) -> None:
    """Delete the product"""
    try:
        await ProductRepository.delete(product_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))