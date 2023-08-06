from dataclasses import dataclass
from typing import TypedDict

class MarketOrderResponse(TypedDict):
    order_id: str

@dataclass
class MarketOrderRequest:
    pair: str
    type: str
    base_account_id: int
    counter_account_id: int
    base_volume: str = None
    counter_volume: str = None
    timestamp: int = None
    ttl: int = 10000
    client_order_id: str = None