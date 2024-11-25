from pydantic   import BaseModel
from typing     import Optional

from core.utils import to_camelcase
from core.crud  import CRUDSchema

# Basic
class CategoryBase(BaseModel):
    name       : str
    description: Optional[str]
    is_show    : bool

    class Config:
        alias_generator  = to_camelcase
        populate_by_name = True
        from_attributes  = True

# GET, GET by ID
class CategoryGet(CategoryBase):
    id: int

# POST
class CategoryCreate(CategoryBase):
    pass

# DELETE
class CategoryDelete(CategoryBase):
    pass

# PUT
class CategoryUpdate(CategoryBase):
    pass

# PATCH
class CategoryPartialUpdate(CategoryBase):
    name       : Optional[str]
    description: Optional[str]
    is_show    : Optional[bool]


class CategorySchema(CRUDSchema):
    get      = CategoryGet
    create   = CategoryCreate
    update   = CategoryUpdate
    p_update = CategoryPartialUpdate
    delete   = CategoryDelete