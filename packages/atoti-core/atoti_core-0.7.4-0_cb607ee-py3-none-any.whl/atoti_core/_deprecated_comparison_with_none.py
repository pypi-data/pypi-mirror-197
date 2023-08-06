from typing import Any

from .deprecated import deprecated


def deprecated_comparison_with_none(value: Any, /, *, invert: bool = False) -> None:
    if value is not None:
        return

    deprecated(
        f"""`object {"!=" if invert else "=="} None` is deprecated, use `{"~" if invert else ""}object.isnull()` instead."""
    )
