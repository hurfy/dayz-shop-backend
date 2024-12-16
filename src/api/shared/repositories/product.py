from uuid                     import UUID

from api.shop.schemas.product import ProductPrice, ProductResponse, ProductCreate, ProductUpdate
from api.shop.models.category import MCategory
from api.shop.models.product  import MProduct
from api.crud.repository      import CRUDMixin, ReadListMixin
from database                 import new_session


class ProductRepository(CRUDMixin, ReadListMixin):
    async def _create_response(self, object_data: MProduct) -> ProductResponse:
        """..."""
        object_data.price = ProductPrice.model_validate(
            {
                "original" : object_data.original_price,
                "surcharge": object_data.surcharge,
            }
        )

        return self.schemas.response.model_validate(object_data)

    async def create(self, object_data: ProductCreate) -> ProductResponse:
        """Create an object in database ..."""
        async with new_session() as session:
            # Does the category exists?
            await self._get_object_or_404(
                model=MCategory,
                object_id=object_data.category_id,
                session=session,
            )

            data = object_data.model_dump(mode="json")

            # Create a model object and add it to the session
            obj = self.model(**data)
            session.add(obj)

            await session.flush()
            await session.commit()

            return await self._create_response(obj)

    async def update(
            self, object_id: UUID, object_data: ProductCreate | ProductUpdate, partial: bool
    ) -> ProductResponse:
        """Update or partial update the object in database ..."""
        async with new_session() as session:
            obj = await self._get_object_or_404(
                object_id=object_id,
                session=session,
            )

            # Does the category exists?
            await self._get_object_or_404(
                model=MCategory,
                object_id=object_data.category_id,
                session=session,
            )

            # Modifying the data
            data = object_data.model_dump(exclude_unset=partial, mode="json")
            for key, value in data.items():
                setattr(obj, key, value)

            await session.commit()

            return await self._create_response(obj)
