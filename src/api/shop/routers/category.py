from fastapi               import APIRouter, status, HTTPException
from typing                import List

from api.shop.repositories import CategoryRepository
from api.shop.schemas      import CategoryGet, CategoryCreate, CategoryUpdate, CategoryPartialUpdate
from core.utils            import HTTP_RESPONSES

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[CategoryGet],
)
async def get_category_list() -> list[CategoryGet]:
    """Get list of categories"""
    return await CategoryRepository.fetch_list()


@router.get(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryGet,
    responses={
            404: HTTP_RESPONSES[404],
    },
)
async def get_category(category_id: int) -> CategoryGet:
    """Get category by ID"""
    try:
        return await CategoryRepository.fetch(
            object_id=category_id,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryCreate,
)
async def create_category(category_data: CategoryCreate) -> CategoryGet:
    """Create a category"""
    return await CategoryRepository.create(
        object_data=category_data,
    )


@router.put(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryGet,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def update_category(category_id: int, category_data: CategoryUpdate) -> CategoryGet:
    """Update the category"""
    try:
        return await CategoryRepository.update(
            object_id=category_id,
            object_data=category_data,
            partial=False,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryGet,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def partial_update_category(category_id: int, category_data: CategoryUpdate) -> CategoryGet:
    """Partial update the category"""
    try:
        return await CategoryPartialUpdate.update(
            object_id=category_id,
            object_data=category_data,
            partial=True,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    path="/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def delete_category(category_id: int) -> None:
    """Delete the category"""
    try:
        await CategoryRepository.delete(
            object_id=category_id,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))