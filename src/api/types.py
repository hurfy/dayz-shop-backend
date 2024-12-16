from pydantic      import BaseModel
from typing        import TypeVar

from api.exception import ResourceNotFoundException
from database      import Model

__all__ = ["TypeModel", "TypeException", "TypeSchema"]

TypeException = TypeVar("TypeException", bound=ResourceNotFoundException)
TypeSchema    = TypeVar("TypeSchema", bound=BaseModel)
TypeModel     = TypeVar("TypeModel", bound=Model)
