from api.crud.routers.category import router as categories_router
from api.crud.routers.product  import router as products_router
from api.crud.routers.order    import router as orders_router

__all__ = [
    "categories_router",
    "products_router",
    "orders_router",
]
