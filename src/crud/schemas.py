from pydantic import BaseModel
from typing   import Generic, TypeVar, Type

TypeBaseScheme   = TypeVar("TypeBaseScheme",   bound=BaseModel)
TypeGetScheme    = TypeVar("TypeGetScheme",    bound=BaseModel)
TypeCreateScheme = TypeVar("TypeCreateScheme", bound=BaseModel)
TypeUpdateScheme = TypeVar("TypeUpdateScheme", bound=BaseModel)


class CRUDSchema(Generic[TypeBaseScheme, TypeGetScheme, TypeCreateScheme, TypeUpdateScheme]):
    base   = Type[TypeBaseScheme]
    get    = Type[TypeGetScheme]
    create = Type[TypeCreateScheme]
    update = Type[TypeUpdateScheme]
