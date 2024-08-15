from typing import Any

from pytest_matchers.matchers import Eq, Matcher
from pytest_matchers.utils.repr_utils import concat_reprs, non_capitalized


class Between(Matcher):
    def __init__(
        self,
        min_value: Any,
        max_value: Any,
        inclusive: bool = None,
        min_inclusive: bool = None,
        max_inclusive: bool = None,
    ):
        if min_value is None and max_value is None:
            raise ValueError("At least one of min or max must be specified")
        self._min = min_value
        self._max = max_value
        if inclusive is not None and (min_inclusive is not None or max_inclusive is not None):
            raise ValueError("Cannot specify inclusive and min_inclusive or max_inclusive")
        if inclusive is not None:
            min_inclusive, max_inclusive = inclusive, inclusive
        self._min_inclusive = min_inclusive or min_inclusive is None
        self._max_inclusive = max_inclusive or max_inclusive is None

    def __new__(cls, min_value, max_value, inclusive=None, min_inclusive=None, max_inclusive=None):
        if min_value is not None and min_value == max_value:
            return Eq(min_value)
        return super().__new__(cls)

    def matches(self, value: Any) -> bool:
        try:
            return self._matches_min(value) and self._matches_max(value)
        except TypeError:
            return False

    def _matches_min(self, value: Any) -> bool:
        if self._min is None:
            return True
        if self._min_inclusive:
            return value >= self._min
        return value > self._min

    def _matches_max(self, value: Any) -> bool:
        if self._max is None:
            return True
        if self._max_inclusive:
            return value <= self._max
        return value < self._max

    def _suffix_repr(self) -> str:
        if self._min and self._max:
            if self._min_inclusive and self._max_inclusive:
                return f"between {self._min} and {self._max}"
            if not self._min_inclusive and not self._max_inclusive:
                return f"between {self._min} and {self._max} exclusive"
        min_repr = self._min_repr()
        max_repr = self._max_repr()
        suffix = concat_reprs("", min_repr, max_repr)
        return non_capitalized(suffix)

    def __repr__(self) -> str:
        return f"To be {self._suffix_repr()}"

    def concatenated_repr(self) -> str:
        return self._suffix_repr()

    def _min_repr(self):
        if not self._min:
            return ""
        return (
            f"greater or equal than {self._min}"
            if self._min_inclusive
            else f"greater than {self._min}"
        )

    def _max_repr(self):
        if not self._max:
            return ""
        return (
            f"lower or equal than {self._max}" if self._max_inclusive else f"lower than {self._max}"
        )
