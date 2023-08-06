from __future__ import annotations

from typing import Literal, Optional, Union, overload

from ._deprecated_comparison_with_none import deprecated_comparison_with_none
from ._other_coordinates import OtherCoordinatesT
from .constant import Constant, ConstantValue
from .has_coordinates import CoordinatesT, HasCoordinates
from .operation import (
    ComparisonCondition,
    Condition,
    OperandConvertible,
    Operation,
    convert_to_operand,
)


class OperandConvertibleWithCoordinates(
    OperandConvertible[CoordinatesT],
    HasCoordinates[CoordinatesT],
):
    """This class overrides `OperandConvertible`'s `Condition`-creating methods so that the type of the returned `Condition`'s `subject` is narrowed down to an instance of `Coordinates` instead of a `Union[Coordinates, Operation]`.

    The returned `Condition`'s `target` is also kept as narrow as possible thanks to `@overload`s.
    """

    # Without this, the classes inheriting from this class are considered unhashable.
    def __hash__(self) -> int:  # pylint: disable=useless-super-delegation
        return super().__hash__()

    def isnull(
        self,
    ) -> Condition[CoordinatesT, Literal["eq"], None, None]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="eq",
            target=None,
        )

    @property
    def _operation_operand(self) -> CoordinatesT:
        return self._coordinates

    # The signature is not compatible with `object.__eq__()` on purpose.
    @overload  # type: ignore[override]
    def __eq__(
        self, other: None, /
    ) -> Condition[CoordinatesT, Literal["eq"], None, None]:
        ...

    @overload
    def __eq__(
        self, other: ConstantValue, /
    ) -> Condition[CoordinatesT, Literal["eq"], Constant, None]:
        ...

    @overload
    def __eq__(
        self, other: HasCoordinates[OtherCoordinatesT], /
    ) -> Condition[CoordinatesT, Literal["eq"], OtherCoordinatesT, None,]:
        ...

    @overload
    def __eq__(
        self,
        other: Optional[
            Union[
                ConstantValue,
                HasCoordinates[OtherCoordinatesT],
                Operation[OtherCoordinatesT],
            ]
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["eq"],
        Optional[Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]]],
        None,
    ]:
        ...

    # The signature is not compatible with `object.__eq__()` on purpose.
    def __eq__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: Optional[
            Union[
                ConstantValue,
                HasCoordinates[OtherCoordinatesT],
                Operation[OtherCoordinatesT],
            ]
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["eq"],
        Optional[Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]]],
        None,
    ]:
        deprecated_comparison_with_none(other)
        return ComparisonCondition(
            subject=self._operation_operand,
            target=convert_to_operand(other),
            operator="eq",
        )

    @overload
    def __ge__(
        self, other: ConstantValue, /
    ) -> Condition[CoordinatesT, Literal["ge"], Constant, None]:
        ...

    @overload
    def __ge__(
        self, other: HasCoordinates[OtherCoordinatesT], /
    ) -> Condition[CoordinatesT, Literal["ge"], OtherCoordinatesT, None,]:
        ...

    @overload
    def __ge__(
        self,
        other: Union[
            ConstantValue,
            HasCoordinates[OtherCoordinatesT],
            Operation[OtherCoordinatesT],
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["ge"],
        Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]],
        None,
    ]:
        ...

    def __ge__(
        self,
        other: Union[
            ConstantValue,
            HasCoordinates[OtherCoordinatesT],
            Operation[OtherCoordinatesT],
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["ge"],
        Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]],
        None,
    ]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="ge",
            target=convert_to_operand(other),
        )

    @overload
    def __gt__(
        self, other: ConstantValue, /
    ) -> Condition[CoordinatesT, Literal["gt"], Constant, None]:
        ...

    @overload
    def __gt__(
        self, other: HasCoordinates[OtherCoordinatesT], /
    ) -> Condition[CoordinatesT, Literal["gt"], OtherCoordinatesT, None,]:
        ...

    @overload
    def __gt__(
        self,
        other: Union[
            ConstantValue,
            HasCoordinates[OtherCoordinatesT],
            Operation[OtherCoordinatesT],
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["gt"],
        Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]],
        None,
    ]:
        ...

    def __gt__(
        self,
        other: Union[
            ConstantValue,
            HasCoordinates[OtherCoordinatesT],
            Operation[OtherCoordinatesT],
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["gt"],
        Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]],
        None,
    ]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="gt",
            target=convert_to_operand(other),
        )

    @overload
    def __le__(
        self, other: ConstantValue, /
    ) -> Condition[CoordinatesT, Literal["le"], Constant, None]:
        ...

    @overload
    def __le__(
        self, other: HasCoordinates[OtherCoordinatesT], /
    ) -> Condition[CoordinatesT, Literal["le"], OtherCoordinatesT, None,]:
        ...

    @overload
    def __le__(
        self,
        other: Union[
            ConstantValue,
            HasCoordinates[OtherCoordinatesT],
            Operation[OtherCoordinatesT],
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["le"],
        Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]],
        None,
    ]:
        ...

    def __le__(
        self,
        other: Union[
            ConstantValue,
            HasCoordinates[OtherCoordinatesT],
            Operation[OtherCoordinatesT],
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["le"],
        Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]],
        None,
    ]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="le",
            target=convert_to_operand(other),
        )

    @overload
    def __lt__(
        self, other: ConstantValue, /
    ) -> Condition[CoordinatesT, Literal["lt"], Constant, None]:
        ...

    @overload
    def __lt__(
        self, other: HasCoordinates[OtherCoordinatesT], /
    ) -> Condition[CoordinatesT, Literal["lt"], OtherCoordinatesT, None,]:
        ...

    @overload
    def __lt__(
        self,
        other: Union[
            ConstantValue,
            HasCoordinates[OtherCoordinatesT],
            Operation[OtherCoordinatesT],
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["lt"],
        Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]],
        None,
    ]:
        ...

    def __lt__(
        self,
        other: Union[
            ConstantValue,
            HasCoordinates[OtherCoordinatesT],
            Operation[OtherCoordinatesT],
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["lt"],
        Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]],
        None,
    ]:
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="lt",
            target=convert_to_operand(other),
        )

    # The signature is not compatible with `object.__ne__()` on purpose.
    @overload  # type: ignore[override]
    def __ne__(
        self, other: None, /
    ) -> Condition[CoordinatesT, Literal["ne"], None, None]:
        ...

    @overload
    def __ne__(
        self, other: ConstantValue, /
    ) -> Condition[CoordinatesT, Literal["ne"], Constant, None]:
        ...

    @overload
    def __ne__(
        self, other: HasCoordinates[OtherCoordinatesT], /
    ) -> Condition[CoordinatesT, Literal["ne"], OtherCoordinatesT, None,]:
        ...

    @overload
    def __ne__(
        self,
        other: Optional[
            Union[
                ConstantValue,
                HasCoordinates[OtherCoordinatesT],
                Operation[OtherCoordinatesT],
            ]
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["ne"],
        Optional[Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]]],
        None,
    ]:
        ...

    # The signature is not compatible with `object.__ne__()` on purpose.
    def __ne__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: Optional[
            Union[
                ConstantValue,
                HasCoordinates[OtherCoordinatesT],
                Operation[OtherCoordinatesT],
            ]
        ],
        /,
    ) -> Condition[
        CoordinatesT,
        Literal["ne"],
        Optional[Union[Constant, OtherCoordinatesT, Operation[OtherCoordinatesT]]],
        None,
    ]:
        deprecated_comparison_with_none(other, invert=True)
        return ComparisonCondition(
            subject=self._operation_operand,
            operator="ne",
            target=convert_to_operand(other),
        )
