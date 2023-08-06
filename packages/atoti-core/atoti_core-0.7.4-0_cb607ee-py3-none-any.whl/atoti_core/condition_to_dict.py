from typing import Dict, Literal, Optional

from .condition_to_pairs import condition_to_pairs
from .has_coordinates import CoordinatesT
from .operation import Condition, ConditionTargetT


def condition_to_dict(
    condition: Condition[
        CoordinatesT,
        Literal["eq"],
        ConditionTargetT,
        Optional[Literal["and"]],
    ],
    /,
) -> Dict[CoordinatesT, ConditionTargetT]:
    pairs = condition_to_pairs(condition)
    result: Dict[CoordinatesT, ConditionTargetT] = {}

    for coordinates, target in pairs:
        if coordinates in result:
            raise ValueError(
                f"Expected the combined condition to have distinct subjects but got `{coordinates}` twice."
            )

        result[coordinates] = target

    return result
