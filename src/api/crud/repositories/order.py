from api.shop.schemas import OrderSchema
from api.shop.models  import MOrder
from api.crud         import CRUDMixin, GetListMixin


class OrderRepository(CRUDMixin, GetListMixin):
    model  = MOrder
    schema = OrderSchema
