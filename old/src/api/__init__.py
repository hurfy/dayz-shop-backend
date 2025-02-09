from api.crud.routers.category import router as categories_crud_router
from api.crud.routers.product  import router as products_crud_router
from api.crud.routers.order    import router as orders_crud_router
from api.shop.routers.order    import router as orders_router

__all__ = [
    "categories_crud_router",
    "products_crud_router",
    "orders_crud_router",
    "orders_router",
]
