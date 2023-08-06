from dataclasses import dataclass
from typing import FrozenSet, Literal, NoReturn, Tuple, Type

from .combine_conditions import combine_conditions
from .constant import Constant
from .coordinates import Coordinates
from .hierarchy_coordinates import HierarchyCoordinates
from .keyword_only_dataclass import keyword_only_dataclass
from .level_coordinates import LevelCoordinates
from .operation import ComparisonCondition, Condition, ConditionCombinationOperatorBound


@keyword_only_dataclass
@dataclass(frozen=True)
class HierarchyIsinCondition(
    Condition[HierarchyCoordinates, Literal["isin"], Constant, None]
):
    subject: HierarchyCoordinates
    level_names: Tuple[str, ...]
    member_paths: Tuple[Tuple[Constant, ...], ...]

    def __post_init__(self) -> None:
        if not self.member_paths:
            raise ValueError(
                "No passed member paths, the condition will always evaluate to `False`."
            )

        for member_path in self.member_paths:
            if not member_path:
                raise ValueError(
                    "Passed one empty member path: it is unnecessary since it will always evaluate to `False`."
                )

            if len(member_path) > len(self.level_names):
                raise ValueError(
                    f"Member path `{tuple(member.value for member in member_path)}` contains more than {len(self.level_names)} elements which is the number of levels of `{repr(self.subject)}`."
                )

    @property
    def combined_comparison_condition(
        self,
    ) -> Condition[
        LevelCoordinates, Literal["eq"], Constant, ConditionCombinationOperatorBound
    ]:
        return combine_conditions(
            [
                [
                    ComparisonCondition(
                        subject=LevelCoordinates(
                            self.subject.dimension_name,
                            self.subject.hierarchy_name,
                            level_name,
                        ),
                        operator="eq",
                        target=member,
                    )
                    for level_name, member in zip(self.level_names, member_path)
                ]
                for member_path in self.member_paths
            ]
        )

    @property
    def _coordinates_classes(self) -> FrozenSet[Type[Coordinates]]:
        return frozenset([type(self.subject)])

    def __invert__(
        self,
    ) -> NoReturn:
        raise RuntimeError(f"A `{type(self).__name__}` cannot be inverted.")
        # It can actually be done using `~hierarchy_isin_condition.combined_comparison_condition` but this changes the type of `subject` which breaks the contract of `Condition.__invert__()`.

    def __repr__(self) -> str:
        return f"{repr(self.subject)}.isin{repr(tuple(tuple(member.value for member in member_path) for member_path in self.member_paths))}"
