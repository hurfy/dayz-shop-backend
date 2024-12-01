from pydantic import BaseModel
from typing   import Generic, TypeVar, Type

TypeGetScheme    = TypeVar("TypeGetScheme",    bound=BaseModel)
TypeCreateScheme = TypeVar("TypeCreateScheme", bound=BaseModel)
TypeUpdateScheme = TypeVar("TypeUpdateScheme", bound=BaseModel)


class CRUDSchema(Generic[TypeGetScheme, TypeCreateScheme, TypeUpdateScheme]):
    get    = Type[TypeGetScheme]
    create = Type[TypeCreateScheme]
    update = Type[TypeUpdateScheme]
