from api.shop.schemas import CategorySchema
from api.shop.models  import MCategory
from crud             import CRUDRepositoryMixin, GetListRepositoryMixin, TypeORM, TypeSchema


class CategoryRepository(CRUDRepositoryMixin, GetListRepositoryMixin):
    model  = MCategory
    schema = CategorySchema

    @classmethod
    async def create_response_data(cls, object_data: TypeORM) -> TypeSchema:
        return cls.schema.get.model_validate(object_data)