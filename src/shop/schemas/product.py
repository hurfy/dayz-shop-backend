from pydantic import BaseModel, HttpUrl, UUID4
from typing   import Optional, Any

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

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        """Converting HttpUrl to str"""
        dumped = super().model_dump(*args, **kwargs)

        # Exist?
        if dumped.get("image_url", None) is not None:
            dumped["image_url"] = str(dumped["image_url"])

        return dumped

# GET, GET by ID
class SProductGet(SProductBase):
    id: UUID4

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