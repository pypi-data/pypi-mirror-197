from __future__ import annotations

from abc import abstractmethod
from datetime import timedelta
from typing import Any, Generic, Iterable, Literal, Optional, TypeVar

import pandas as pd

from .base_hierarchies import BaseHierarchiesBound
from .base_level import BaseLevel
from .base_levels import BaseLevelsBound, HierarchiesT
from .base_measure import BaseMeasure
from .base_measures import BaseMeasuresBound
from .context import Context
from .empty_mapping import EMPTY_MAPPING
from .query_filter import QueryFilter
from .repr_json import ReprJson, ReprJsonable
from .scenario import BASE_SCENARIO_NAME

LevelsT = TypeVar("LevelsT", bound=BaseLevelsBound, covariant=True)
MeasuresT = TypeVar("MeasuresT", bound=BaseMeasuresBound, covariant=True)


class BaseCube(
    Generic[HierarchiesT, LevelsT, MeasuresT],
    ReprJsonable,
):
    def __init__(
        self, name: str, /, *, hierarchies: HierarchiesT, measures: MeasuresT
    ) -> None:
        super().__init__()

        self._hierarchies = hierarchies
        self._measures = measures
        self._name = name

    @property
    def name(self) -> str:
        """Name of the cube."""
        return self._name

    @property
    @abstractmethod
    def levels(self) -> LevelsT:
        """Levels of the cube."""

    @property
    def measures(self) -> MeasuresT:
        """Measures of the cube."""
        return self._measures

    @property
    def hierarchies(self) -> HierarchiesT:
        """Hierarchies of the cube."""
        return self._hierarchies

    @abstractmethod
    def query(
        self,
        *measures: BaseMeasure,
        context: Context = EMPTY_MAPPING,
        filter: Optional[QueryFilter] = None,  # pylint: disable=redefined-builtin
        include_totals: bool = False,
        levels: Iterable[BaseLevel] = (),
        mode: Literal["pretty", "raw"] = "pretty",
        scenario: str = BASE_SCENARIO_NAME,
        timeout: timedelta = timedelta(seconds=30),
        **kwargs: Any,
    ) -> pd.DataFrame:
        ...

    def _repr_json_(self) -> ReprJson:
        return (
            {
                "Dimensions": self.hierarchies._repr_json_()[0],
                "Measures": self.measures._repr_json_()[0],
            },
            {"expanded": False, "root": self.name},
        )


BaseCubeBound = BaseCube[BaseHierarchiesBound, BaseLevelsBound, BaseMeasuresBound]
