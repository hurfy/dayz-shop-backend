from fastapi               import APIRouter, HTTPException, status, Path
from typing                import List
from uuid                  import UUID

from api.shop.repositories import ProductRepository
from api.shop.schemas      import ProductGet, ProductCreate, ProductUpdate, ProductPartialUpdate
from core.utils            import HTTP_RESPONSES

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[ProductGet],
)
async def get_product_list() -> list[ProductGet]:
    """Get list of products"""
    return await ProductRepository.fetch_list()


@router.get(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductGet,
    responses={
            404: HTTP_RESPONSES[404],
    },
)
async def get_product(product_id: UUID = Path(..., format="uuid")) -> ProductGet:
    """Get product by ID"""
    try:
        return await ProductRepository.fetch(
            object_id=product_id
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductGet,
)
async def create_product(product_data: ProductCreate) -> ProductGet:
    """Create a product"""
    # return await ProductRepository.create_product(product_data)
    return await ProductRepository.create(
        object_data=product_data,
    )


@router.put(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductGet,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def update_product(
        product_data: ProductUpdate, product_id: UUID = Path(..., format="uuid")
) -> ProductGet:
    """Update the product"""
    try:
        return await ProductRepository.update(
            object_id=product_id,
            object_data=product_data,
            partial=False
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductGet,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def partial_update_product(
        product_data: ProductPartialUpdate, product_id: UUID = Path(..., format="uuid")
) -> ProductGet:
    """Partial update the product"""
    try:
        return await ProductRepository.update(
            object_id=product_id,
            object_data=product_data,
            partial=True
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def delete_product(product_id: UUID = Path(..., format="uuid")) -> None:
    """Delete the product"""
    try:
        await ProductRepository.delete(product_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))