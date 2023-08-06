from typing import Literal, Tuple, cast

from .get_literal_args import get_literal_args

BooleanOperator = Literal["and", "or"]

ALL_BOOLEAN_OPERATORS = cast(
    Tuple[BooleanOperator, ...], get_literal_args(BooleanOperator)
)
