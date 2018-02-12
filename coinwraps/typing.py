from typing import NamedTuple, List, Tuple


OrderPair = List[Tuple[str, int]]


class Orderbook(NamedTuple):
    asks: OrderPair
    bids: OrderPair