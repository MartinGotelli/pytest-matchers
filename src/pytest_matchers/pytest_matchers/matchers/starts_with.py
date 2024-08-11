from typing import Any, Sized

from pytest_matchers.matchers import Matcher


class StartsWith(Matcher):
    def __init__(self, prefix: Sized | str):
        self._prefix = prefix

    def matches(self, value: Any) -> bool:
        if isinstance(value, str):
            try:
                return value.startswith(self._prefix)
            except TypeError:
                return False
        if isinstance(value, list):
            return value[: len(self._prefix)] == self._prefix

        return False

    def __repr__(self) -> str:
        return f"To start with {repr(self._prefix)}"

    def concatenated_repr(self) -> str:
        return f"starting with {repr(self._prefix)}"
