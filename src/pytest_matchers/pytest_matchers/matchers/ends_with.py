from typing import Any, Sized

from pytest_matchers.matchers import Matcher


class EndsWith(Matcher):
    def __init__(self, suffix: Sized | str):
        self._suffix = suffix

    def matches(self, value: Any) -> bool:
        if isinstance(value, str):
            try:
                return value.endswith(self._suffix)
            except TypeError:
                return False
        if isinstance(value, list):
            suffix_len = len(self._suffix)
            return value[-suffix_len:] == self._suffix

        return False

    def __repr__(self) -> str:
        return f"To end with {repr(self._suffix)}"

    def concatenated_repr(self) -> str:
        return f"ending with {repr(self._suffix)}"
