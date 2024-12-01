from pydantic   import BaseModel, Field
from typing     import Optional

from decorators import optional
from api.utils  import to_camelcase
from crud       import CRUDSchema


class CategoryBase(BaseModel):
    name: str = Field(
        max_length=256,
        title="Category name",
        examples=["weapon"],
    )
    description: Optional[str] = Field(
        default=None,
        max_length=512,
        title="Category description",
        examples=["better guns in all of chernarus"],
    )
    is_show: bool = Field(
        title="Is the category visible",
        examples=[True],
    )

    class Config:
        alias_generator  = to_camelcase
        populate_by_name = True
        from_attributes  = True


class CategoryResponse(CategoryBase):
    id: int = Field(
        gt=0,
        title="Category ID",
        examples=["12"],
    )


class CategoryCreate(CategoryBase):
    """Сan use this for a complete upgrade"""
    ...


@optional()
class CategoryUpdate(CategoryBase):
    ...


class CategorySchema(CRUDSchema):
    get    = CategoryResponse
    create = CategoryCreate
    update = CategoryUpdate