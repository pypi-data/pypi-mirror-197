from abc import abstractmethod
from typing import Literal, Optional

from .measure_coordinates import MeasureCoordinates
from .operand_convertible_with_coordinates import OperandConvertibleWithCoordinates
from .operation import ComparisonCondition, Condition


class BaseMeasure(OperandConvertibleWithCoordinates[MeasureCoordinates]):
    def __init__(self, name: str, /) -> None:
        super().__init__()

        self._name = name

    @property
    def name(self) -> str:
        """Name of the measure."""
        return self._name

    @property
    @abstractmethod
    def folder(self) -> Optional[str]:
        """Folder of the measure."""

    @property
    @abstractmethod
    def visible(self) -> bool:
        """Whether the measure is visible or not."""

    @property
    @abstractmethod
    def description(self) -> Optional[str]:
        """Description of the measure."""

    @property
    @abstractmethod
    def formatter(self) -> Optional[str]:
        """Formatter of the measure."""

    def isnull(self) -> Condition[MeasureCoordinates, Literal["eq"], None, None]:
        """Return a condition evaluating to ``True`` if the measure evalutes to ``None`` and ``False`` otherwise.

        Use ``~measure.isnull()`` for the opposite behavior.

        Example:

            >>> df = pd.DataFrame(
            ...     columns=["Country", "City", "Price"],
            ...     data=[
            ...         ("France", "Paris", 200.0),
            ...         ("Germany", "Berlin", None),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, table_name="isnull example")
            >>> cube = session.create_cube(table)
            >>> l, m = cube.levels, cube.measures
            >>> m["Price.isnull"] = m["Price.SUM"].isnull()
            >>> m["Price.notnull"] = ~m["Price.SUM"].isnull()
            >>> cube.query(
            ...     m["Price.isnull"],
            ...     m["Price.notnull"],
            ...     levels=[l["Country"]],
            ... )
                    Price.isnull Price.notnull
            Country
            France         False          True
            Germany         True         False

        """
        return ComparisonCondition(
            subject=self._operation_operand, operator="eq", target=None
        )

    @property
    def _coordinates(self) -> MeasureCoordinates:
        return MeasureCoordinates(self.name)

    @property
    def _operation_operand(self) -> MeasureCoordinates:
        return self._coordinates
