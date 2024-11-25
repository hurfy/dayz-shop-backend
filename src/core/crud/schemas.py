from pydantic import BaseModel
from typing   import Generic, TypeVar, Type

TypeGetScheme     = TypeVar("TypeGetScheme",     bound=BaseModel)
TypeCreateScheme  = TypeVar("TypeCreateScheme",  bound=BaseModel)
TypeUpdateScheme  = TypeVar("TypeUpdateScheme",  bound=BaseModel)
TypePUpdateScheme = TypeVar("TypePUpdateScheme", bound=BaseModel)
TypeDeleteScheme  = TypeVar("TypeDeleteScheme",  bound=BaseModel)


class CRUDSchema(
    Generic[TypeGetScheme, TypeCreateScheme, TypeUpdateScheme, TypePUpdateScheme, TypeDeleteScheme]
):
    get      = Type[TypeGetScheme]
    create   = Type[TypeCreateScheme]
    update   = Type[TypeUpdateScheme]
    p_update = Type[TypePUpdateScheme]
    delete   = Type[TypeDeleteScheme]