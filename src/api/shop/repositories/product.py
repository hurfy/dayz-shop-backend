from api.shop.schemas import ProductSchema, ProductPriceResponse
from api.shop.models  import MProduct
from crud             import CRUDRepositoryMixin, GetListRepositoryMixin, TypeSchema, TypeORM


class ProductRepository(CRUDRepositoryMixin, GetListRepositoryMixin):
    model  = MProduct
    schema = ProductSchema

    @classmethod
    async def create_response_data(cls, object_data: TypeORM) -> TypeSchema:
        object_data.price = ProductPriceResponse.model_validate(
            {
                "original" : object_data.original_price,
                "surcharge": object_data.surcharge,
            }
        )

        return cls.schema.get.model_validate(object_data)