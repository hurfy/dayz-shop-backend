from pydantic import BaseModel, HttpUrl
from typing   import Optional

from utils    import to_camelcase


# Basic
class SProductBase(BaseModel):
    name           : str
    purchase_price : int
    selling_price  : int
    count          : int
    description    : Optional[str]
    category_id    : int
    image_url      : HttpUrl
    is_show        : bool

    class Config:
        alias_generator  = to_camelcase
        populate_by_name = True
        from_attributes  = True


# GET, GET by ID
class SProductGet(SProductBase):
    id: int

# POST,
class SProductCreate(SProductBase):
    pass

# PUT
class SProductUpdate(SProductBase):
    pass

# PATCH
class SProductPartialUpdate(SProductBase):
    name          : Optional[str]     = None
    purchase_price: Optional[int]     = None
    selling_price : Optional[int]     = None
    count         : Optional[int]     = None
    description   : Optional[str]     = None
    category_id   : Optional[int]     = None
    image_url     : Optional[HttpUrl] = None
    is_show       : Optional[bool]    = None