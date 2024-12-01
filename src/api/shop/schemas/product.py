from pydantic        import BaseModel, Field, HttpUrl, UUID4, computed_field
from typing          import Optional, Any

from api.shop.models import ProductType
from decorators      import optional
from api.utils       import to_camelcase
from crud            import CRUDSchema


PRICE_FIELD = Field(
    ge=0,
    title="Original price from the in-game merchant",
    examples=[24000000],
)
SURCHARGE_FIELD = Field(
    gt=0,
    title="Product surcharge",
    description="The surcharge cannot be less than 0. Otherwise, the final price will not be calculated correctly.",
    examples=[10],
)


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
    description: Optional[str] = Field(
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

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        """Converting HttpUrl to str"""
        dumped = super().model_dump(*args, **kwargs)

        # Exist?
        if dumped.get("image_url", None) is not None:
            dumped["image_url"] = str(dumped["image_url"])

        return dumped


class ProductPriceResponse(BaseModel):
    original : int = PRICE_FIELD
    surcharge: int = SURCHARGE_FIELD

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
        title="Product ID",
        description="Can convert `strings` to actual `UUID` automatically",
        examples=["3f2504e0-4f89-11d3-9a0c-0305e82c3301"],
    )
    price: ProductPriceResponse


class ProductCreate(ProductBase):
    """Сan use this for a complete upgrade"""
    original_price: int = PRICE_FIELD
    surcharge     : int = SURCHARGE_FIELD


@optional()
class ProductUpdate(ProductCreate):
    pass


class ProductSchema(CRUDSchema):
    get    = ProductResponse
    create = ProductCreate
    update = ProductUpdate