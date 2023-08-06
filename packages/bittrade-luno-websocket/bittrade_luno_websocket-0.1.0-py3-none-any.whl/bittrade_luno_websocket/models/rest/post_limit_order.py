
from dataclasses import dataclass

@dataclass
class LimitOrderRequest:
    base: str
    counter: str
    type: str
    volume: str
    price: str
    pair: str
    post_only: bool = False
    time_in_force: str = "GTC"
    stop_price: str = None
    stop_direction: str = None
    client_order_id: str = None

