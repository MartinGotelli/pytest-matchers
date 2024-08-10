from typing import Any, Sized

from src.matchers import Matcher


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
            return value[-len(self._suffix) :] == self._suffix

        return False

    def __repr__(self) -> str:
        return f"To end with {repr(self._suffix)}"

    def concatenated_repr(self) -> str:
        return f"ending with {repr(self._suffix)}"
