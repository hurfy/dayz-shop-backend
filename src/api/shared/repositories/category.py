from api.shop.schemas.category import CategorySchema
from api.shop.models.category  import MCategory
from api.crud.repository       import CRUDMixin, GetListMixin


class CategoryRepository(CRUDMixin, GetListMixin):
    model  = MCategory
    schema = CategorySchema
