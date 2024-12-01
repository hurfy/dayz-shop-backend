from sqlalchemy       import select
from uuid             import UUID

from api.shop.schemas import ProductSchema, ProductPriceResponse, ProductResponse, ProductCreate, ProductUpdate
from api.shop.models  import MProduct, MCategory
from database         import new_session
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

    @classmethod
    async def create(cls, object_data: ProductCreate) -> ProductResponse:
        """Create an object in database ..."""
        async with new_session() as session:
            category = await session.execute(
                select(MCategory).filter(MCategory.id == object_data.category_id)
            )

            # Doest the category exist? (HTTP 404)
            if not category.scalar_one_or_none():
                raise ValueError(f"category with id {object_data.category_id} not found")

            data = object_data.model_dump()

            # Create a model object and add it to the session
            obj = cls.model(**data)
            session.add(obj)

            await session.flush()
            await session.commit()

            return await cls.create_response_data(obj)

    @classmethod
    async def update(
            cls, object_id: UUID, object_data: ProductCreate | ProductUpdate, partial: bool
    ) -> ProductResponse:
        """Update or partial update the object in database ..."""
        async with new_session() as session:
            query = await session.execute(
                select(cls.model).where(object_id == cls.model.id)
            )

            # Does the object exist? (HTTP 404)
            if not (obj := query.scalars().first()):
                raise ValueError(f"{cls.model.__name__[1:].lower()} with id {object_id} not found")

            category = await session.execute(
                select(MCategory).filter(MCategory.id == object_data.category_id)
            )

            # Doest the category exist? (HTTP 404)
            if not category.scalar_one_or_none():
                raise ValueError(f"category with id {object_data.category_id} not found")

            # Modifying the data
            data = object_data.model_dump(exclude_unset=partial)
            for key, value in data.items():
                setattr(obj, key, value)

            await session.commit()

            return await cls.create_response_data(obj)