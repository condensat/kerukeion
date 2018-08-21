# the inclusion of the test module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "test" package
from engine import Engine
from order import Order
from hamcrest import *


def test_simple_full_match():
    e = Engine()

    s1 = Order(type=Order.Type.SELL, quantity=5, timestamp=0)

    assert_that(calling(Engine.process_order).with_args(e, s1), raises(Exception))


def test_double_buy_match():
    e = Engine()

    s1 = Order(type=Order.Type.SELL, price=568, quantity=5, timestamp=0)
    s2 = Order(type=Order.Type.SELL, price=432, quantity=5, timestamp=0)
    b1 = Order(type=Order.Type.BUY, quantity=5, timestamp=0)

    processed_result = e.process_order(s1)

    assert_that(e.get_spread(), equal_to((None, 568)))
    assert_that(processed_result, equal_to([]))

    processed_result = e.process_order(s2)

    assert_that(e.get_spread(), equal_to((None, 432)))
    assert_that(processed_result, equal_to([]))

    processed_result = e.process_order(b1)

    assert_that(e.get_spread(), equal_to((None, 568)))
    assert_that(processed_result, equal_to([(b1, s2)]))
