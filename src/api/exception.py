from uuid import UUID
from re   import findall


class ResourceNotFoundException(Exception):
    def __init__(self, id_: int | UUID) -> None:
        self.id = id_

    def __str__(self) -> str:
        resource_name = findall(
            r"[A-Z]?[^A-Z]*", self.__class__.__name__
        )[0]

        return f"{resource_name} with id {self.id} not found"


class CategoryNotFoundError(ResourceNotFoundException):
    ...


class ProductNotFoundError(ResourceNotFoundException):
    ...


class OrderNotFoundError(ResourceNotFoundException):
    ...
