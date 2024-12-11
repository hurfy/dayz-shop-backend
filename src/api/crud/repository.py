from sqlalchemy      import select
from fastapi         import HTTPException
from typing          import TypeVar, Generic
from uuid            import UUID
from abc             import ABC, ABCMeta

from api.crud.schema import CRUDSchema
from database        import Model, new_session

__all__ = [
    "CRUDMixin", "GetMixin", "GetListMixin", "CreateMixin", "UpdateMixin", "DeleteMixin", "TypeORM", "TypeSchema"
]


TypeORM    = TypeVar("TypeORM",    bound=Model)
TypeSchema = TypeVar("TypeSchema", bound=CRUDSchema)


class RepositoryBase(Generic[TypeORM, TypeSchema], ABC):
    model  = type[TypeORM]
    schema = type[TypeSchema]

    @classmethod
    async def response_data(cls, object_data: TypeORM) -> TypeSchema:
        """This method implements a way to serialize data from database objects into a response schema"""
        return cls.schema.response.model_validate(object_data)


class CreateMixin(RepositoryBase, metaclass=ABCMeta):
    @classmethod
    async def create(cls, object_data: TypeSchema) -> TypeSchema:
        """Create an object in database ..."""
        async with new_session() as session:
            data = object_data.model_dump(mode="json")

            # Create a model object and add it to the session
            obj = cls.model(**data)
            session.add(obj)

            await session.flush()
            await session.commit()

            return await cls.response_data(obj)


class GetMixin(RepositoryBase, metaclass=ABCMeta):
    @classmethod
    async def fetch(cls, object_id: int | UUID) -> TypeSchema:
        """Fetch an object from database ..."""
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

            return await cls.response_data(obj)


class UpdateMixin(RepositoryBase, metaclass=ABCMeta):
    @classmethod
    async def update(cls, object_id: int | UUID, object_data: TypeSchema, partial: bool) -> TypeSchema:
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

            # Modifying the data
            data = object_data.model_dump(exclude_unset=partial, mode="json")
            for key, value in data.items():
                setattr(obj, key, value)

            await session.commit()

            return await cls.response_data(obj)


class DeleteMixin(RepositoryBase, metaclass=ABCMeta):
    @classmethod
    async def delete(cls, object_id: int | UUID) -> None:
        """Delete an object from database ..."""
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

            await session.delete(obj)
            await session.commit()


class GetListMixin(RepositoryBase, metaclass=ABCMeta):
    @classmethod
    async def fetch_list(cls) -> list[TypeSchema]:
        """Fetch the list of objects from database ..."""
        async with new_session() as session:
            query = await session.execute(
                select(cls.model)
            )

            # Extract all objects from query result
            as_dict = query.scalars().all()

            # Serialize each object to pydantic scheme
            return [await cls.response_data(each) for each in as_dict]


class CRUDMixin(
    CreateMixin, GetMixin, UpdateMixin, DeleteMixin,
    metaclass=ABCMeta
):
    ...
