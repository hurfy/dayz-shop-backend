from pydantic  import BaseModel

from api.types import TypeModel, TypeSchema, TypeException

__all__ = ["CRUDSchema", "RepositoryConfig"]


class CRUDSchema(BaseModel):
    response: type[TypeSchema]
    create  : type[TypeSchema]
    update  : type[TypeSchema]


class RepositoryConfig(BaseModel):
    model    : type[TypeModel]
    schemas  : CRUDSchema
    exception: type[TypeException]
