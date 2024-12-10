from pydantic import BaseModel
from fastapi  import Path
from typing   import TypeVar, Annotated

Model = TypeVar("Model", bound=type[BaseModel])


# Path
uuid_ = Annotated[str, Path(
    default          = ...,
    min_length       = 32,
    max_length       = 36,
    pattern          = r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$",
    title            = "UUID",
    description      = "FastAPI can convert `strings` to actual `UUID` automatically",
    openapi_examples = {
        "valid"  : {
            "summary": "Valid data",
            "value"  : "3f2504e0-4f89-11d3-9a0c-0305e82c3301",
        },
        "invalid": {
            "summary": "Invalid data",
            "value"  : "123e4567-e89b-12d3-a456-42665544000012",
        },
    },
)]

id_ = Annotated[int, Path(
    default = ...,
    gt      = 0,
    title   = "ID",
    description      = "Numeric identifier",
    openapi_examples = {
        "valid"  : {
            "summary": "Valid data",
            "value"  : 12,
        },
        "invalid": {
            "summary": "Invalid data",
            "value"  : -34,
        },
    },
)]


# Query
# ...

# Body
# ...
