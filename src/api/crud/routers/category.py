from fastapi               import APIRouter, status

from api.crud.repositories import CategoryRepository
from api.shop.schemas      import CategoryResponse, CategoryCreate, CategoryUpdate
from api.utils             import HTTP_RESPONSES
from params                import Model, id_

router = APIRouter(
    prefix = "/categories",
    tags   = ["Categories"],
)


# Get data -------------------------------------------------------------------------------------------------------------
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryResponse],
)
async def get_category_list() -> list[CategoryResponse]:
    """Get list of categories"""
    return await CategoryRepository.fetch_list()


@router.get(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
    responses={
            404: HTTP_RESPONSES[404],
    },
)
async def get_category(category_id: id_) -> CategoryResponse:
    """Get category by ID"""
    return await CategoryRepository.fetch(
        object_id=category_id,
    )


# Create data ----------------------------------------------------------------------------------------------------------
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse,
)
async def create_category(category_data: CategoryCreate) -> CategoryResponse:
    """Create a category"""
    return await CategoryRepository.create(
        object_data=category_data,
    )


# Update data ----------------------------------------------------------------------------------------------------------
async def update_category_base(
        category_data: type[Model], category_id: id_, partial: bool = False
) -> CategoryResponse:
    return await CategoryRepository.update(
        object_id=category_id,
        object_data=category_data,
        partial=partial,
    )


@router.put(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def update_category(category_data: CategoryCreate, category_id: id_) -> CategoryResponse:
    """Update the category"""
    return await update_category_base(category_data, category_id, partial=False)


@router.patch(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def partial_update_category(category_data: CategoryUpdate, category_id: id_) -> CategoryResponse:
    """Partial update the category"""
    return await update_category_base(category_data, category_id, partial=True)


# Delete data ----------------------------------------------------------------------------------------------------------
@router.delete(
    path="/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: HTTP_RESPONSES[404],
    },
)
async def delete_category(category_id: id_) -> None:
    """Delete the category"""
    await CategoryRepository.delete(
        object_id=category_id,
    )
