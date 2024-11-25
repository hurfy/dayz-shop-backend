from pydantic        import BaseModel, HttpUrl, UUID4, computed_field
from typing          import Optional, Any

from api.shop.models import ProductType
from core.utils      import to_camelcase
from core.crud       import CRUDSchema


# Basic
class ProductBase(BaseModel):
    name             : str
    category_id      : int
    surcharge        : int
    original_price   : int
    type             : ProductType
    count            : int
    description      : Optional[str]
    image_url        : HttpUrl
    is_discount_apply: bool
    is_show          : bool

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
class ProductGet(ProductBase):
    id: UUID4

    @computed_field
    @property
    def price(self) -> int:
        """Calculates the final cost of the product, taking into account surcharge"""
        if self.surcharge == 0:
            return self.original_price

        return int(self.original_price * (1 + self.surcharge / 100))

# POST
class ProductCreate(ProductBase):
    pass

# DELETE
class ProductDelete(ProductBase):
    pass

# PUT
class ProductUpdate(ProductBase):
    pass

# PATCH
class ProductPartialUpdate(ProductBase):
    name             : Optional[str]     = None
    category_id      : Optional[int]     = None
    surcharge        : Optional[int]     = None
    original_price   : Optional[int]     = None
    type             : Optional[ProductType] = None
    count            : Optional[int]     = None
    description      : Optional[str]     = None
    image_url        : Optional[HttpUrl] = None
    is_discount_apply: Optional[bool]    = None
    is_show          : Optional[bool]    = None


class ProductSchema(CRUDSchema):
    get      = ProductGet
    create   = ProductCreate
    update   = ProductUpdate
    p_update = ProductPartialUpdate
    delete   = ProductDelete