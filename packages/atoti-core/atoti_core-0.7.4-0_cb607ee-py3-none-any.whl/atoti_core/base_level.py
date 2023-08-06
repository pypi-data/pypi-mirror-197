from __future__ import annotations

from abc import abstractmethod
from typing import Literal

from .constant import Constant, ConstantValue
from .isin_condition import IsinCondition
from .level_coordinates import LevelCoordinates
from .operand_convertible_with_coordinates import OperandConvertibleWithCoordinates
from .operation import ComparisonCondition, Condition
from .repr_json import ReprJson, ReprJsonable


class BaseLevel(
    OperandConvertibleWithCoordinates[LevelCoordinates],
    ReprJsonable,
):
    def __init__(self, name: str, /) -> None:
        super().__init__()

        self._name = name

    @property
    def name(self) -> str:
        """Name of the level."""
        return self._name

    @property
    @abstractmethod
    def dimension(self) -> str:
        """Name of the dimension holding the level."""

    @property
    @abstractmethod
    def hierarchy(self) -> str:
        """Name of the hierarchy holding the level."""

    @property
    def _coordinates(self) -> LevelCoordinates:
        return LevelCoordinates(self.dimension, self.hierarchy, self._name)

    @property
    def _operation_operand(self) -> LevelCoordinates:
        return self._coordinates

    def isin(
        self, *members: ConstantValue
    ) -> Condition[LevelCoordinates, Literal["isin"], Constant, None]:
        """Return a condition to check that the level is on one of the given members.

        ``level.isin(a, b)`` is equivalent to ``(level == a) | (level == b)``.

        Args:
            members: One or more members on which the level should be.

        Example:
            .. doctest:: Level.isin

                >>> df = pd.DataFrame(
                ...     columns=["City", "Price"],
                ...     data=[
                ...         ("Berlin", 150.0),
                ...         ("London", 240.0),
                ...         ("New York", 270.0),
                ...         ("Paris", 200.0),
                ...     ],
                ... )
                >>> table = session.read_pandas(
                ...     df, keys=["City"], table_name="isin example"
                ... )
                >>> cube = session.create_cube(table)
                >>> l, m = cube.levels, cube.measures
                >>> m["Price.SUM in London and Paris"] = tt.filter(
                ...     m["Price.SUM"], l["City"].isin("London", "Paris")
                ... )
                >>> cube.query(
                ...     m["Price.SUM"],
                ...     m["Price.SUM in London and Paris"],
                ...     levels=[l["City"]],
                ... )
                         Price.SUM Price.SUM in London and Paris
                City
                Berlin      150.00
                London      240.00                        240.00
                New York    270.00
                Paris       200.00                        200.00

            .. doctest:: Level.isin
                :hide:

                Clear the session to isolate the multiple methods sharing this docstring.
                >>> session._clear()

        """
        return IsinCondition(
            subject=self._operation_operand,
            elements=tuple(Constant(member) for member in members),
        )

    def isnull(  # pylint: disable=useless-super-delegation
        self,
    ) -> Condition[LevelCoordinates, Literal["eq"], None, None]:
        """Return a condition evaluating to ``True`` when a level is not expressed in a query and ``False`` otherwise.

        Use `~level.isnull()` for the opposite behavior.

        Example:

            >>> df = pd.DataFrame(
            ...     columns=["Country", "City", "Price"],
            ...     data=[
            ...         ("France", "Paris", 200.0),
            ...         ("Germany", "Berlin", 120),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, table_name="isnull example")
            >>> cube = session.create_cube(table)
            >>> l, m = cube.levels, cube.measures
            >>> m["City.isnull"] = l["City"].isnull()
            >>> m["City.notnull"] = ~l["City"].isnull()
            >>> cube.query(
            ...     m["City.isnull"],
            ...     m["City.notnull"],
            ...     levels=[l["Country"], l["City"]],
            ...     include_totals=True,
            ... )
                           City.isnull City.notnull
            Country City
            Total                 True        False
            France                True        False
                    Paris        False         True
            Germany               True        False
                    Berlin       False         True

        """
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="eq",
            target=None,
        )

    @abstractmethod
    def _repr_json_(self) -> ReprJson:
        """JSON representation of the level."""
