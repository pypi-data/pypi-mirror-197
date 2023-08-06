import dataclasses
from typing import Callable
import reactivex
import requests
from bittrade_luno_websocket.models.rest.post_market_order import MarketOrderRequest, MarketOrderResponse
from bittrade_luno_websocket.connection.http import prepare_request, send_request
from bittrade_luno_websocket.models import RequestMessage
from bittrade_luno_websocket.models import endpoints
from bittrade_luno_websocket.rest.get_order import get_order_http, GetOrderRequest
from reactivex import operators, compose


def post_market_order_http(request: MarketOrderRequest, add_token: Callable) -> reactivex.Observable[MarketOrderResponse]:
    return send_request(
        add_token(
            prepare_request(RequestMessage(
            method="POST",
            endpoint=endpoints.Endpoints.POST_MARKET_ORDER,
            params=dataclasses.asdict(request),
        )
    )))

def load_order_details(add_token: Callable):
    return compose(
        operators.flat_map(lambda x: get_order_http(GetOrderRequest(id=x["order_id"]), add_token)),
    )
