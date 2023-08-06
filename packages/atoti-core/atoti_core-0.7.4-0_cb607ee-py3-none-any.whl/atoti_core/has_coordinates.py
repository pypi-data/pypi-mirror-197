from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .coordinates import Coordinates

CoordinatesT = TypeVar("CoordinatesT", bound=Coordinates, covariant=True)


class HasCoordinates(Generic[CoordinatesT], ABC):
    @property
    @abstractmethod
    def _coordinates(self) -> CoordinatesT:
        ...


HasCoordinatesBound = HasCoordinates[Coordinates]
