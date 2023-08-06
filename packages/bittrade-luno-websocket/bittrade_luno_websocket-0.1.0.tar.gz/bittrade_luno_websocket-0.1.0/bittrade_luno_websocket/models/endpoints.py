from enum import Enum

class Endpoints(Enum):
    """Enum class for all the endpoints"""
    GET_ORDER_V3 = '/api/exchange/3/order'
    POST_MARKET_ORDER = '/api/1/marketorder'
    ORDERBOOK_TOP = '/api/1/orderbook_top'