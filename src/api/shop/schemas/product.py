from pydantic        import BaseModel, Field, HttpUrl, UUID4, computed_field
from typing          import Annotated

from api.shop.models import ProductType
from decorators      import optional
from api.utils       import to_camelcase
from api.shared      import CRUDSchema

__all__ = ["ProductBase", "ProductSchema", "ProductResponse", "ProductCreate", "ProductUpdate", "ProductPriceResponse"]


price = Annotated[int, Field(
    ge=0,
    title="Original price from the in-game merchant",
    examples=[24000000],
)]
surcharge = Annotated[int, Field(
    gt=0,
    title="Product surcharge",
    description="The surcharge cannot be less than 0. Otherwise, the final price will not be calculated correctly.",
    examples=[10],
)]


class ProductBase(BaseModel):
    name: str = Field(
        max_length=256,
        title="Product name",
        examples=["Doom Slayer Toy"],
    )
    category_id: int = Field(
        gt=0,
        title="Category ID",
        examples=[24],
    )
    type: ProductType = Field(
        title="Product type",
        examples=["purchase", "sell"],
    )
    count: int = Field(
        ge=0,
        title="Product count in stock",
        examples=[1],
    )
    description: str | None = Field(
        default=None,
        max_length=512,
        title="Product description",
        examples=["I wanna be your Slayer"],
    )
    image_url: HttpUrl = Field(
        title="Product image URL",
        examples=["https://image.com/doom_slayer_toy.jpg"],
    )
    is_discount_apply: bool = Field(
        title="Whether a purchase discount can be applied",
        examples=[True],
    )
    is_show: bool = Field(
        title="Is the product visible",
        examples=[True],
    )

    class Config:
        alias_generator  = to_camelcase
        populate_by_name = True
        from_attributes  = True


class ProductPriceResponse(BaseModel):
    original : price
    surcharge: surcharge

    @computed_field(
        description="Final cost of the product, taking into account surcharge",
        examples=["26400000"],
    )
    @property
    def final(self) -> int:
        """Calculates the final cost of the product, taking into account surcharge"""
        if self.surcharge == 0:
            return self.original

        return int(self.original * (1 + self.surcharge / 100))


class ProductResponse(ProductBase):
    id: UUID4 = Field(
        title="Product id",
        description="Can convert `strings` to actual `UUID` automatically",
        examples=["3f2504e0-4f89-11d3-9a0c-0305e82c3301"],
    )
    price: ProductPriceResponse


class ProductCreate(ProductBase):
    """Сan use this for a complete upgrade"""
    original_price: price
    surcharge     : surcharge


@optional()
class ProductUpdate(ProductCreate):
    ...


class ProductSchema(CRUDSchema):
    response = ProductResponse
    create   = ProductCreate
    update   = ProductUpdate
