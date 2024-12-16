from fastapi                          import APIRouter, Depends, status, HTTPException
from typing                           import Annotated

from api.shared.repositories.category import CategoryRepository
from api.shop.schemas.category        import CategoryResponse, CategoryCreate, CategoryUpdate
from api.dependencies                 import category_repository
from api.utils                        import HTTP_RESPONSES
from params                           import Model, Pid

router = APIRouter(
    prefix = "/categories",
    tags   = ["Categories"],
)

repository: type[CategoryRepository] = Annotated[CategoryRepository, Depends(category_repository)]


# Get data -------------------------------------------------------------------------------------------------------------
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryResponse],
    description="Get a non-paginated list of categories",
)
async def read_list(repo: repository) -> list[CategoryResponse]:
    """Get list of categories"""
    return await repo.read_list()


@router.get(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
    responses={
            404: HTTP_RESPONSES[404],
    },
    description="Get category by id",
)
async def read(
        repo: repository, category_id: Pid
) -> CategoryResponse:
    """Get category by id"""
    try:
        return await repo.read(category_id)

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# Create data ----------------------------------------------------------------------------------------------------------
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse,
    description="Create new category",
)
async def create(
        repo: repository, category_data: CategoryCreate
) -> CategoryResponse:
    """Create new category"""
    return await repo.create(object_data=category_data)


# Update data ----------------------------------------------------------------------------------------------------------
async def update_base(
        repo: CategoryRepository, category_data: type[Model], category_id: Pid, partial: bool = False
) -> CategoryResponse:
    """update_category_base ..."""
    return await repo.update(
        object_id=category_id, object_data=category_data, partial=partial,
    )


@router.put(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Update category by id",
)
async def update(
        repo: repository, category_data: CategoryCreate, category_id: Pid
) -> CategoryResponse:
    """Update category by id"""
    try:
        return await update_base(
            repo, category_data, category_id, partial=False
        )

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.patch(
    path="/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Partial update a category",
)
async def partial_update(
        repo: repository, category_data: CategoryUpdate, category_id: Pid
) -> CategoryResponse:
    """Partial update category by id"""
    try:
        return await update_base(
            repo, category_data, category_id, partial=True
        )

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# Delete data ----------------------------------------------------------------------------------------------------------
@router.delete(
    path="/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        404: HTTP_RESPONSES[404],
    },
    description="Delete category",
)
async def delete(
        repo: repository, category_id: Pid
) -> None:
    """Delete category by id"""
    try:
        return await repo.delete(category_id)

    except repo.exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
