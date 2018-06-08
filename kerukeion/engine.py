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
        self._bid: SortedKeyList[Order] = SortedKeyList(key=lambda o: "{}{}".format(o.price, to_bin(-o.timestamp)))
        self._ask: SortedKeyList[Order] = SortedKeyList(
            key=lambda o: "{}{}".format(to_bin(-o.price), to_bin(-o.timestamp)))

    def match_against_queue(self, order: Order) -> List[Tuple[Order, Order]]:
        in_queue: SortedKeyList[Order]
        out_queue: SortedKeyList[Order]
        test_price_range: Callable[[Order, Order], bool]

        if order.type & Order.Type.BUY:
            in_queue = self._ask
            out_queue = self._bid
            test_price_range = lambda o1, o2: o1.limit <= o1.price
        elif order.type & Order.Type.SELL:
            in_queue = self._bid
            out_queue = self._ask
            test_price_range = lambda o1, o2: o1.limit >= o1.price

        if in_queue:
            if test_price_range(order, in_queue[0]):
                matched_order: Order = in_queue.pop()
                if order.quantity > matched_order.quantity:
                    new_smaller_order = order._replace(quantity=order.quantity - matched_order.quantity)
                    return [(order, matched_order)] + self.match_against_queue(new_smaller_order)
                else:
                    if matched_order.quantity > order.quantity:
                        new_smaller_order = matched_order._replace(quantity=matched_order.quantity - order.quantity)
                        in_queue.append(new_smaller_order)
                    return [(order, matched_order)]
            out_queue.append(order)

    def process_order(self, order: Order) -> List[Tuple[Order, Union[Order, None]]]:
        if order.type & Order.Type.CANCEL:
            if order.type & Order.Type.BUY:
                self._bid.remove(order)
            elif order.type & Order.Type.SELL:
                self._ask.remove(order)
            return [(order, None)]
        return self.match_against_queue(order)


if __name__ == '__main__':
    e = Engine()
