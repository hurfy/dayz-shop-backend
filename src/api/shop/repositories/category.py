from api.shop.schemas import CategorySchema
from api.shop.models  import MCategory
from core.crud        import CRUDRepositoryMixin

class CategoryRepository(CRUDRepositoryMixin):
    model  = MCategory
    schema = CategorySchema
