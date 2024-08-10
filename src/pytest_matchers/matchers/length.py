from typing import Any

from pytest_matchers.matchers import Matcher


class Length(Matcher):
    def __init__(self, length=None, min_length=None, max_length=None):
        if length:
            if min_length or max_length:
                raise ValueError("Cannot specify length with min_length or max_length")
            min_length = length
            max_length = length
        self._min_length = min_length
        self._max_length = max_length

    def matches(self, value: Any) -> bool:
        try:
            value_length = len(value)
        except TypeError:
            return False
        matches_min = self._min_length <= value_length if self._min_length else True
        matches_max = value_length <= self._max_length if self._max_length else True
        return matches_min and matches_max

    def _length_repr(self) -> str:
        if self._min_length is not None and self._max_length is not None:
            if self._min_length == self._max_length:
                return f"of {self._min_length}"
            return f"between {self._min_length} and {self._max_length}"
        if self._min_length is not None:
            return f"greater or equal than {self._min_length}"
        if self._max_length is not None:
            return f"lower or equal than {self._max_length}"
        return ""

    def concatenated_repr(self) -> str:
        length_repr = self._length_repr()
        if length_repr:
            return f"with length {length_repr}"
        return length_repr

    def __repr__(self) -> str:
        length_repr = self._length_repr()
        if length_repr:
            return f"To have length {length_repr}"
        return length_repr
