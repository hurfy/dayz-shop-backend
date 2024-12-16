from api.shared.repositories.category import CategoryRepository
from api.shared.repositories.product  import ProductRepository
from api.shared.repositories.order    import OrderRepository
from api.shop.schemas.category        import category_schema
from api.shop.schemas.product         import product_schema
from api.shop.models.category         import MCategory
from api.shop.models.product          import MProduct
from api.shop.schemas.order           import order_schema
from api.shop.models.order            import MOrder
from api.crud.schemas                 import RepositoryConfig
from api.exception                    import CategoryNotFoundError, ProductNotFoundError, OrderNotFoundError


async def category_repository() -> CategoryRepository:
    """Dependency, returns CategoryRepository"""
    return CategoryRepository(
        config=RepositoryConfig(
            model=MCategory,
            schemas=category_schema,
            exception=CategoryNotFoundError
        )
    )

async def product_repository() -> ProductRepository:
    """Dependency, returns ProductRepository"""
    return ProductRepository(
        config=RepositoryConfig(
            model=MProduct,
            schemas=product_schema,
            exception=ProductNotFoundError,
        )
    )

async def order_repository() -> OrderRepository:
    """Dependency, returns OrderRepository"""
    return OrderRepository(
        config=RepositoryConfig(
            model=MOrder,
            schemas=order_schema,
            exception=OrderNotFoundError,
        )
    )
