from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from .coordinates import Coordinates
from .hierarchy_coordinates import HierarchyCoordinates


@dataclass(frozen=True)
class LevelCoordinates(Coordinates):  # pylint: disable=keyword-only-dataclass
    dimension_name: str
    hierarchy_name: str
    level_name: str

    @property
    def key(self) -> Tuple[str, str, str]:
        return self.dimension_name, self.hierarchy_name, self.level_name

    @cached_property
    def hierarchy_coordinates(self) -> HierarchyCoordinates:
        return HierarchyCoordinates(self.dimension_name, self.hierarchy_name)

    def __repr__(self) -> str:
        return f"l[{self.key}]"
