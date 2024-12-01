from sqlalchemy   import select
from typing       import TypeVar, Generic, Type
from uuid         import UUID
from abc          import ABC, abstractmethod, ABCMeta

from crud.schemas import CRUDSchema
from database     import Model, new_session


TypeORM    = TypeVar("TypeORM",    bound=Model)
TypeSchema = TypeVar("TypeSchema", bound=CRUDSchema)


class RepositoryBase(Generic[TypeORM, TypeSchema], ABC):
    model  = Type[TypeORM]
    schema = Type[TypeSchema]

    @classmethod
    @abstractmethod
    async def create_response_data(cls, object_data: TypeORM) -> TypeSchema:
        """This abstract method implements a way to serialize data from database objects into a response schema"""
        ...


class CreateRepositoryMixin(RepositoryBase, metaclass=ABCMeta):
    @classmethod
    async def create(cls, object_data: TypeSchema) -> TypeSchema:
        """Create an object in database ..."""
        async with new_session() as session:
            data = object_data.model_dump()

            # Create a model object and add it to the session
            obj = cls.model(**data)
            session.add(obj)

            await session.flush()
            await session.commit()

            return await cls.create_response_data(obj)


class GetRepositoryMixin(RepositoryBase, metaclass=ABCMeta):
    @classmethod
    async def fetch(cls, object_id: int | UUID) -> TypeSchema:
        """Fetch an object from database ..."""
        async with new_session() as session:
            query = await session.execute(
                select(cls.model).where(object_id == cls.model.id)
            )

            # Does the object exist? (HTTP 404)
            if not (obj := query.scalars().first()):
                raise ValueError(f"{cls.model.__name__[1:].lower()} with id {object_id} not found")

            return await cls.create_response_data(obj)


class UpdateRepositoryMixin(RepositoryBase, metaclass=ABCMeta):
    @classmethod
    async def update(cls, object_id: int | UUID, object_data: TypeSchema, partial: bool) -> TypeSchema:
        """Update or partial update the object in database ..."""
        async with new_session() as session:
            query = await session.execute(
                select(cls.model).where(object_id == cls.model.id)
            )

            # Does the object exist? (HTTP 404)
            if not (obj := query.scalars().first()):
                raise ValueError(f"{cls.model.__name__[1:].lower()} with id {object_id} not found")

            # Modifying the data
            data = object_data.model_dump(exclude_unset=partial)
            for key, value in data.items():
                setattr(obj, key, value)

            await session.commit()

            return await cls.create_response_data(obj)


class DeleteRepositoryMixin(RepositoryBase, metaclass=ABCMeta):
    @classmethod
    async def delete(cls, object_id: int | UUID) -> None:
        """Delete an object from database ..."""
        async with new_session() as session:
            query = await session.execute(
                select(cls.model).where(object_id == cls.model.id)
            )

            # Does the object exist? (HTTP 404)
            if not (obj := query.scalars().first()):
                raise ValueError(f"{cls.model.__name__[1:].lower()} with id {object_id} not found")

            await session.delete(obj)
            await session.commit()


class GetListRepositoryMixin(RepositoryBase, metaclass=ABCMeta):
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
            return [await cls.create_response_data(each) for each in as_dict]


class CRUDRepositoryMixin(
    CreateRepositoryMixin, GetRepositoryMixin, UpdateRepositoryMixin, DeleteRepositoryMixin,
    metaclass=ABCMeta
):
    ...