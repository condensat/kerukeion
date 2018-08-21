import uuid
from enum import IntFlag, unique, auto
from typing import NamedTuple


class Order(NamedTuple):

    @unique
    class Type(IntFlag):
        BUY = auto()
        SELL = auto()
        CANCEL = auto()

    timestamp: int
    type: Type
    quantity: int
    price: int = None
    id = uuid.uuid4()
