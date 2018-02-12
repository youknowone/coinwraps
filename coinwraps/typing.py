from typing import NamedTuple, List, Tuple
from decimal import Decimal
import datetime
import ciso8601


OrderPair = List[Tuple[str, int]]


class Orderbook(NamedTuple):
    asks: OrderPair
    bids: OrderPair


class HistoryItem(NamedTuple):
    id: str
    str_filled_at: str
    fill_type: str
    order_type: str
    price: Decimal
    quantity: Decimal
    total: Decimal

    @property
    def filled_at(self) -> datetime.datetime:
        return ciso8601.parse_datetime(self.str_filled_at)
