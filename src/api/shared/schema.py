from pydantic import BaseModel
from typing   import Generic, TypeVar

__all__ = ["CRUDSchema"]

TypeResponseScheme = TypeVar("TypeResponseScheme", bound=BaseModel)
TypeCreateScheme   = TypeVar("TypeCreateScheme", bound=BaseModel)
TypeUpdateScheme   = TypeVar("TypeUpdateScheme", bound=BaseModel)


class CRUDSchema(Generic[TypeResponseScheme, TypeCreateScheme, TypeUpdateScheme]):
    response = type[TypeResponseScheme]
    create   = type[TypeCreateScheme]
    update   = type[TypeUpdateScheme]
