from sqlalchemy        import select
from typing            import TypeVar, Generic, Type
from uuid              import UUID

from core.crud.schemas import CRUDSchema
from core.database     import Model, new_session


TypeORM    = TypeVar("TypeORM",    bound=Model)
TypeSchema = TypeVar("TypeSchema", bound=CRUDSchema)


class CRUDRepositoryMixin(Generic[TypeORM, TypeSchema]):
    model  = Type[TypeORM]
    schema = Type[TypeSchema]

    @classmethod
    async def fetch_list(cls) -> list[TypeSchema]:
        """Fetch the list of objects from database ..."""
        async with new_session() as session:
            # Execute SQL query to fetch all data from database
            query = await session.execute(
                select(cls.model)
            )

            # Extract all objects from query result
            as_dict = query.scalars().all()

            # Serialize objects to pydantic scheme
            return [cls.schema.get.model_validate(each) for each in as_dict]

    @classmethod
    async def fetch(cls, object_id: int | UUID) -> TypeSchema:
        """Fetch an object from database ..."""
        async with new_session() as session:
            # Execute SQL query to fetch an object from the database
            query = await session.execute(
                select(cls.model).where(object_id == cls.model.id)
            )

            # Does the object exist? (HTTP 404)
            if not (obj := query.scalars().first()):
                raise ValueError(f"{cls.model.__name__[1:].lower()} with ID {object_id} not found")

            return cls.schema.get.model_validate(obj)

    @classmethod
    async def create(cls, object_data: TypeSchema) -> TypeSchema:
        """Create an object in database ..."""
        async with new_session() as session:
            # Object data as a python dictionary
            data = object_data.model_dump()

            # Create a model object and add it to the session
            obj = cls.model(**data)
            session.add(obj)

            # Applying the changes
            await session.flush()
            await session.commit()

            return cls.schema.get.model_validate(obj)

    @classmethod
    async def update(cls, object_id: int | UUID, object_data: TypeSchema, partial: bool) -> TypeSchema:
        """Update or partial update the object in database ..."""
        async with new_session() as session:
            # Execute SQL query to fetch an object from the database
            query = await session.execute(
                select(cls.model).where(object_id == cls.model.id)
            )

            # Does the object exist? (HTTP 404)
            if not (obj := query.scalars().first()):
                raise ValueError(f"{cls.model.__name__[1:].lower()} with ID {object_id} not found")

            # Object data as a python dictionary
            data = object_data.model_dump(exclude_unset=partial)

            # Modifying the data
            for key, value in data.items():
                setattr(obj, key, value)

            # Applying the changes
            await session.commit()

            return cls.schema.get.model_validate(obj)

    @classmethod
    async def delete(cls, object_id: int | UUID) -> None:
        """Delete an object from database ..."""
        async with new_session() as session:
            # Execute SQL query to fetch an object from the database
            query = await session.execute(
                select(cls.model).where(object_id == cls.model.id)
            )

            # Does the object exist? (HTTP 404)
            if not (obj := query.scalars().first()):
                raise ValueError(f"{cls.model.__name__[1:].lower()} with ID {object_id} not found")

            # Applying the changes
            await session.delete(obj)
            await session.commit()