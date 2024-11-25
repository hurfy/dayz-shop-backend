from api.shop.schemas import ProductSchema
from api.shop.models  import MProduct
from core.crud    import CRUDRepositoryMixin


class ProductRepository(CRUDRepositoryMixin):
    model  = MProduct
    schema = ProductSchema
