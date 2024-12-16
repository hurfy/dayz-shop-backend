from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy             import select
from uuid                   import UUID

from api.crud.schemas       import RepositoryConfig
from api.types              import TypeModel, TypeSchema
from database               import new_session

__all__ = ["CRUDMixin", "ReadMixin", "ReadListMixin", "CreateMixin", "UpdateMixin", "DeleteMixin",]


class RepositoryBase:
    def __init__(self, config: RepositoryConfig) -> None:
        self.model     = config.model
        self.schemas   = config.schemas
        self.exception = config.exception

    async def _create_response(self, object_data: TypeModel) -> TypeSchema:
        """This method implements a way to serialize data from database objects into a response schema"""
        return self.schemas.response.model_validate(object_data)

    async def _get_object_or_404(
            self, object_id: int | UUID, session: AsyncSession, model: TypeModel | None = None,
    ) -> TypeModel:
        """Returns a db object or 404"""
        model = model or self.model

        query = await session.execute(
            select(model).where(model.id == object_id)
        )

        if not (obj := query.scalars().first()):
            raise self.exception(id_=object_id)

        return obj


class CreateMixin(RepositoryBase):
    async def create(self, object_data: TypeSchema) -> TypeModel:
        """Create an object in database ..."""
        async with new_session() as session:
            data = object_data.model_dump(mode="json")

            # Create a model object and add it to the session
            obj = self.model(**data)
            session.add(obj)

            await session.flush()
            await session.commit()

            return await self._create_response(obj)


class ReadMixin(RepositoryBase):
    async def read(self, object_id: int | UUID) -> TypeModel:
        """Read an object from database ..."""
        async with new_session() as session:
            obj = await self._get_object_or_404(
                object_id=object_id,
                session=session,
            )

            return await self._create_response(obj)


class UpdateMixin(RepositoryBase):
    async def update(
            self, object_id: int | UUID, object_data: TypeSchema, partial: bool
    ) -> TypeModel:
        """Update or partial update the object in database ..."""
        async with new_session() as session:
            obj = await self._get_object_or_404(
                object_id=object_id,
                session=session,
            )

            # Modifying the data
            data = object_data.model_dump(exclude_unset=partial, mode="json")
            for key, value in data.items():
                setattr(obj, key, value)

            await session.commit()

            return await self._create_response(obj)


class DeleteMixin(RepositoryBase):
    async def delete(self, object_id: int | UUID) -> None:
        """Delete an object from database ..."""
        async with new_session() as session:
            obj = await self._get_object_or_404(
                object_id=object_id,
                session=session,
            )

            await session.delete(obj)
            await session.commit()


class ReadListMixin(RepositoryBase):
    async def read_list(self) -> list[TypeModel]:
        """Read the list of objects from database ..."""
        async with new_session() as session:
            query = await session.execute(
                select(self.model)
            )

            # Extract all objects from query result
            as_dict = query.scalars().all()

            # Serialize each object to pydantic scheme
            return [await self._create_response(each) for each in as_dict]


class CRUDMixin(CreateMixin, ReadMixin, UpdateMixin, DeleteMixin):
    ...
