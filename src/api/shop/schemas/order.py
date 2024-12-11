from pydantic              import BaseModel, Field, UUID4
from typing                import Annotated

from api.shop.models.order import EOrderStatus
from api.crud.schema       import CRUDSchema
from decorators            import optional
from api.utils             import to_camelcase

__all__ = ["OrderBase", "OrderSchema", "OrderResponse", "OrderCreate", "OrderUpdate", "OrderItem", "OrderStatus"]

status = Annotated[EOrderStatus, Field(
        title="Order status",
        examples=["waiting", "completed", "canceled"],
)]


class OrderStatus(BaseModel):
    status: status

class OrderItem(BaseModel):
    product_id: UUID4 = Field(
        title="Product ID in the database",
        description="Can convert `strings` to actual `UUID` automatically",
        examples=["e4c5239e-ff3c-45ed-ad55-dd9d3ade12fd"],
    )
    count: int = Field(
        title="Number of items in an order",
        examples=[12],
    )
    price: int = Field(
        title="Total cost of items in the order",
        description="(Original price + surcharge) * count"
    )


class OrderBase(BaseModel):
    status: status
    user_id: UUID4 = Field(
        frozen=True,
        title="Id of user who placed the order",
        description="Can convert `strings` to actual `UUID` automatically",
        examples=["6b2e6db0-5aec-4e4b-a9f0-6ecaa788a349"],
    )
    total: int = Field(
        title="Total cost of order",
        examples=[100000000],
    )
    products: list[OrderItem] = Field(
        title="List of items in the order",
        examples=[
            [
                {
                    "product_id": "fb062bb5-56b0-4d22-b926-381cc3ac8bd6",
                    "count": 24,
                    "price": 1200000,
                }
            ]
        ]
    )


class OrderResponse(OrderBase):
    id: UUID4 = Field(
        title="Order id",
        description="Can convert `strings` to actual `UUID` automatically",
        examples=["3f2504e0-4f89-11d3-9a0c-0305e82c3301"],
    )

    class Config:
        alias_generator  = to_camelcase
        populate_by_name = True
        from_attributes  = True


class OrderCreate(OrderBase):
    """Сan use this for a complete upgrade"""
    ...


@optional(without_fields=["user_id"])
class OrderUpdate(OrderCreate):
    ...


class OrderSchema(CRUDSchema):
    response = OrderResponse
    create   = OrderCreate
    update   = OrderUpdate
