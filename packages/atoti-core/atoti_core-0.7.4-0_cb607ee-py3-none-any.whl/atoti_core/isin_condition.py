from dataclasses import dataclass
from typing import FrozenSet, Literal, Optional, Tuple, Type, TypeVar

from .combine_conditions import combine_conditions
from .constant import Constant
from .coordinates import Coordinates
from .hierarchy_coordinates import HierarchyCoordinates
from .keyword_only_dataclass import keyword_only_dataclass
from .operation import (
    ComparisonCondition,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    ConditionSubjectT,
)

IsinConditionElementT = TypeVar(
    "IsinConditionElementT", bound=Optional[Constant], covariant=True
)


@keyword_only_dataclass
@dataclass(frozen=True)
class IsinCondition(
    Condition[ConditionSubjectT, Literal["isin"], IsinConditionElementT, None]
):
    subject: ConditionSubjectT
    elements: Tuple[IsinConditionElementT, ...]

    def __post_init__(self) -> None:
        assert not isinstance(
            self.subject, HierarchyCoordinates
        ), "Conditions on hierarchies must use `HierarchyIsinCondition`."

        if not self.elements:
            raise ValueError(
                "No passed elements, the condition will always evaluate to `False`."
            )

    @property
    def combined_comparison_condition(
        self,
    ) -> Condition[
        ConditionSubjectT, Literal["eq"], IsinConditionElementT, Optional[Literal["or"]]
    ]:
        return combine_conditions(
            [
                (
                    ComparisonCondition(
                        subject=self.subject, operator="eq", target=element
                    ),
                )
                for element in self.elements
            ]
        )

    @property
    def _coordinates_classes(self) -> FrozenSet[Type[Coordinates]]:
        return self._get_coordinates_classes(self.subject)

    def __invert__(
        self,
    ) -> Condition[
        ConditionSubjectT,
        ConditionComparisonOperatorBound,
        IsinConditionElementT,
        ConditionCombinationOperatorBound,
    ]:
        return ~self.combined_comparison_condition

    def __repr__(self) -> str:
        return f"{repr(self.subject)}.isin{repr(tuple(element.value if isinstance(element, Constant) else element for element in self.elements))}"


IsinConditionBound = IsinCondition[Coordinates, Optional[Constant]]
