from fastapi                  import HTTPException
from sqlalchemy               import select
from uuid                     import UUID

from api.shop.schemas.product import ProductSchema, ProductPrice, ProductResponse, ProductCreate, ProductUpdate
from api.shop.models.category import MCategory
from api.shop.models.product  import MProduct
from database                 import new_session
from api.crud.repository      import CRUDMixin, GetListMixin, TypeSchema


class ProductRepository(CRUDMixin, GetListMixin):
    model  = MProduct
    schema = ProductSchema

    @classmethod
    async def response_data(cls, object_data: MProduct) -> TypeSchema:
        """..."""
        object_data.price = ProductPrice.model_validate(
            {
                "original" : object_data.original_price,
                "surcharge": object_data.surcharge,
            }
        )

        return cls.schema.response.model_validate(object_data)

    @classmethod
    async def create(cls, object_data: ProductCreate) -> ProductResponse:
        """Create an object in database ..."""
        async with new_session() as session:
            category = await session.execute(
                select(MCategory).filter(MCategory.id == object_data.category_id)
            )

            # Doest the category exist? (HTTP 404)
            if not category.scalar_one_or_none():
                raise HTTPException(
                    status_code=404,
                    detail=f"category with id {object_data.category_id} not found"
                )

            data = object_data.model_dump(mode="json")

            # Create a model object and add it to the session
            obj = cls.model(**data)
            session.add(obj)

            await session.flush()
            await session.commit()

            return await cls.response_data(obj)

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
                raise HTTPException(
                    status_code=404,
                    detail=f"{cls.model.__name__[1:].lower()} with id {object_id} not found"
                )

            category = await session.execute(
                select(MCategory).filter(MCategory.id == object_data.category_id)
            )

            # Doest the category exist? (HTTP 404)
            if not category.scalar_one_or_none():
                raise HTTPException(
                    status_code=404,
                    detail=f"category with id {object_data.category_id} not found"
                )

            # Modifying the data
            data = object_data.model_dump(exclude_unset=partial, mode="json")
            for key, value in data.items():
                setattr(obj, key, value)

            await session.commit()

            return await cls.response_data(obj)
