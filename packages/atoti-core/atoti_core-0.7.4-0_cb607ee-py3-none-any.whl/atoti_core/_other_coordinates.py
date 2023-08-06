from typing import TypeVar

from .coordinates import Coordinates

OtherCoordinatesT = TypeVar("OtherCoordinatesT", bound=Coordinates, covariant=True)
