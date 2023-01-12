from brfundamentus.models.constants import OperationType
from pydantic.dataclasses import dataclass
from pydantic import PositiveFloat, PositiveInt


@dataclass
class Operation:
    ticker: str
    price: PositiveFloat
    quantity: PositiveInt
    type: OperationType