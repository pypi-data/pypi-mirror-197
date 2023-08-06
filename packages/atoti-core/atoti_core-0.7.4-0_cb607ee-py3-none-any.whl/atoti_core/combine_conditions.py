from typing import Collection, Literal, Tuple, TypeVar, Union, overload

from .boolean_operator import BooleanOperator
from .operation import (
    CombinedCondition,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionCombinationOperatorT,
    ConditionComparisonOperatorT,
    ConditionSubjectT,
    ConditionTargetT,
)

_BooleanOperatorT = TypeVar("_BooleanOperatorT", bound=BooleanOperator)


def _combine_conditions(
    *conditions: Condition[
        ConditionSubjectT,
        ConditionComparisonOperatorT,
        ConditionTargetT,
        ConditionCombinationOperatorT,
    ],
    operator: _BooleanOperatorT,
) -> Condition[
    ConditionSubjectT,
    ConditionComparisonOperatorT,
    ConditionTargetT,
    Union[ConditionCombinationOperatorT, _BooleanOperatorT],
]:
    if not conditions:
        raise ValueError("No conditions to combine.")

    iterator = iter(conditions)
    condition = next(iterator)

    if len(conditions) == 1:
        return condition

    return CombinedCondition(
        sub_conditions=(
            condition,
            _combine_conditions(*iterator, operator=operator),
        ),
        operator=operator,
    )


@overload
# If the top level collection has a single element, the operator `or` will not be used, only `and`.
def combine_conditions(
    conditions: Tuple[
        Collection[
            Condition[
                ConditionSubjectT,
                ConditionComparisonOperatorT,
                ConditionTargetT,
                ConditionCombinationOperatorT,
            ]
        ]
    ],
    /,
) -> Condition[
    ConditionSubjectT,
    ConditionComparisonOperatorT,
    ConditionTargetT,
    Union[ConditionCombinationOperatorT, Literal["and"]],
]:
    ...


@overload
# If all the bottom level collections have a single element, the operator `and` will not be used, only `or`.
def combine_conditions(
    conditions: Collection[
        Tuple[
            Condition[
                ConditionSubjectT,
                ConditionComparisonOperatorT,
                ConditionTargetT,
                ConditionCombinationOperatorT,
            ]
        ]
    ],
    /,
) -> Condition[
    ConditionSubjectT,
    ConditionComparisonOperatorT,
    ConditionTargetT,
    Union[ConditionCombinationOperatorT, Literal["or"]],
]:
    ...


@overload
def combine_conditions(
    conditions: Collection[
        Collection[
            Condition[
                ConditionSubjectT,
                ConditionComparisonOperatorT,
                ConditionTargetT,
                ConditionCombinationOperatorBound,
            ]
        ]
    ],
    /,
) -> Condition[
    ConditionSubjectT,
    ConditionComparisonOperatorT,
    ConditionTargetT,
    ConditionCombinationOperatorBound,
]:
    ...


def combine_conditions(
    conditions: Collection[
        Collection[
            Condition[
                ConditionSubjectT,
                ConditionComparisonOperatorT,
                ConditionTargetT,
                ConditionCombinationOperatorBound,
            ]
        ]
    ],
    /,
) -> Condition[
    ConditionSubjectT,
    ConditionComparisonOperatorT,
    ConditionTargetT,
    ConditionCombinationOperatorBound,
]:
    """Take conditions structured in disjunctive normal form and return a single combined condition."""
    return _combine_conditions(
        *(
            _combine_conditions(*conjunct_conditions, operator="and")
            for conjunct_conditions in conditions
        ),
        operator="or",
    )
