import pydantic.fields

from pydantic import BaseModel, create_model
from typing   import Optional, Type, Any, Callable
from copy     import deepcopy

from database import Model




def optional(without_fields: list[str] | None = None) -> Callable[[Model], Model]:
    """Make all pydantic model fields optional"""
    # It is better not to use a mutable object as a default parameter, so we use the following construction:
    if without_fields is None:
        without_fields = []

    def wrapper(model: Type[Model]) -> Type[Model]:
        base_model: Type[Model] = model

        def make_field_optional(
            field: pydantic.fields.FieldInfo, default: Any = None
        ) -> tuple[Any, pydantic.fields.FieldInfo]:
            new = deepcopy(field)
            new.default = default
            new.annotation = Optional[field.annotation]

            return new.annotation, new

        if without_fields:
            base_model = BaseModel

        return create_model(
            model.__name__,
            __base__=base_model,
            __module__=model.__module__,
            **{
                field_name: make_field_optional(field_info)
                for field_name, field_info in model.model_fields.items()
                if field_name not in without_fields
            },
        )

    return wrapper