import uuid
from enum import IntFlag, unique, auto
from typing import NamedTuple

from numpy.core import int64, int32


class Order(NamedTuple):

    @unique
    class Type(IntFlag):
        BUY = auto()
        SELL = auto()
        CANCEL = auto()

    timestamp: int64
    type: Type
    quantity: int32
    price: int32
    limit: int32 = -1
    id = uuid.uuid4()
