import logging
from typing import List, Tuple, Callable, Union

from sortedcontainers import SortedKeyList

from kerukeion.order import Order

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def to_bin(nb: int) -> bin:
    return bin(((1 << 32) - 1) & nb)


class Engine:

    def __init__(self):
        self._bid: SortedKeyList[Order] = SortedKeyList(
            key=lambda o: "{}{}".format(to_bin(-o.price), to_bin(-o.timestamp))
        )
        self._ask: SortedKeyList[Order] = SortedKeyList(
            key=lambda o: "{}{}".format(o.price, to_bin(-o.timestamp))
        )

    def _match_against_queue(self, order_to_match: Order) -> List[Tuple[Order, Order]]:
        in_queue: SortedKeyList[Order]
        out_queue: SortedKeyList[Order]
        test_price_range: Callable[[Order, Order], bool]

        if order_to_match.type & Order.Type.BUY:
            in_queue = self._ask
            out_queue = self._bid

            def test_price_range(o1: Order, o2: Order):
                return not o1.price or o1.price <= o2.price

        elif order_to_match.type & Order.Type.SELL:
            in_queue = self._bid
            out_queue = self._ask

            def test_price_range(o1: Order, o2: Order):
                return not o1.price or o1.price >= o2.price

        def _impl(order: Order) -> List[Tuple[Order, Order]]:
            if in_queue:
                if test_price_range(order, in_queue[0]):
                    matched_order: Order = in_queue.pop(0)
                    if order.quantity > matched_order.quantity:
                        new_smaller_order = order._replace(quantity=order.quantity - matched_order.quantity)
                        return [(order, matched_order)] + _impl(new_smaller_order)
                    else:
                        if matched_order.quantity > order.quantity:
                            new_smaller_order = matched_order._replace(quantity=matched_order.quantity - order.quantity)
                            in_queue.add(new_smaller_order)
                        return [(order, matched_order)]
            if not order.price:  # Market order cannot be queued
                raise Exception("Error No Market")  # TODO: make custom exception
            out_queue.add(order)
            return []

        return _impl(order_to_match)

    def process_order(self, order: Order) -> List[Tuple[Order, Union[Order, None]]]:
        if order.type & Order.Type.CANCEL:
            if order.type & Order.Type.BUY:
                self._bid.remove(order)
            elif order.type & Order.Type.SELL:
                self._ask.remove(order)
            return [(order, None)]
        return self._match_against_queue(order)

    def get_spread(self) -> Tuple[Union[int, None], Union[int, None]]:
        return self._bid[0].price if self._bid else None, \
               self._ask[0].price if self._ask else None


if __name__ == '__main__':
    e = Engine()

