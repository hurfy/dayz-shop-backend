from fastapi           import APIRouter, HTTPException, status
from typing            import List

from shop.repositories import ProductRepository
from shop.schemas      import SProductGet, SProductCreate, SProductUpdate, SProductPartialUpdate
from utils             import PRODUCT_RESPONSES

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[SProductGet],
)
async def get_product_list() -> list[SProductGet]:
    """Get list of products"""
    return await ProductRepository.fetch_product_list()


@router.get(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=SProductGet,
    responses={
            404: PRODUCT_RESPONSES[404],
    },
)
async def get_product(product_id: int) -> SProductGet:
    """Get product by ID"""
    try:
        return await ProductRepository.fetch_product(product_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=SProductGet,
)
async def create_product(product_data: SProductCreate) -> SProductGet:
    """Create a product"""
    return await ProductRepository.create_product(product_data)


@router.put(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=SProductGet,
    responses={
        404: PRODUCT_RESPONSES[404],
    },
)
async def update_product(product_id: int, product_data: SProductUpdate) -> SProductGet:
    """Update the product"""
    try:
        return await ProductRepository.update_product(product_id=product_id, product_data=product_data, partial=False)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=SProductGet,
    responses={
        404: PRODUCT_RESPONSES[404],
    },
)
async def partial_update_product(product_id: int, product_data: SProductPartialUpdate) -> SProductGet:
    """Partial update the product"""
    try:
        return await ProductRepository.update_product(product_id=product_id, product_data=product_data, partial=True)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: PRODUCT_RESPONSES[404],
    },
)
async def delete_product(product_id: int) -> None:
    """Delete the product"""
    try:
        await ProductRepository.delete_product(product_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))