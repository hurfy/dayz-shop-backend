from api.shop.schemas import CategorySchema
from api.shop.models  import MCategory
from api.crud         import CRUDMixin, GetListMixin


class CategoryRepository(CRUDMixin, GetListMixin):
    model  = MCategory
    schema = CategorySchema
