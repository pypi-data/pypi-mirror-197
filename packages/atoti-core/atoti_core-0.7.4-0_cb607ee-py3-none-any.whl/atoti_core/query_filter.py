from __future__ import annotations

from typing import Literal, Optional, Union

from .constant import Constant
from .hierarchy_coordinates import HierarchyCoordinates
from .level_coordinates import LevelCoordinates
from .operation import Condition

QueryFilter = Condition[
    Union[HierarchyCoordinates, LevelCoordinates],
    Literal["eq", "isin"],
    Constant,
    Optional[Literal["and"]],
]
