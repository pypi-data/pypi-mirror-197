from dataclasses import dataclass
from typing import Tuple

from .coordinates import Coordinates


@dataclass(frozen=True)
class MeasureCoordinates(Coordinates):  # pylint: disable=keyword-only-dataclass
    measure_name: str

    @property
    def key(self) -> Tuple[str]:
        return (self.measure_name,)

    def __repr__(self) -> str:
        return f"""m["{self.measure_name}"]"""
