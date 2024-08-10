from typing import Any

from pytest_matchers.matchers import Matcher


class Contains(Matcher):
    def __init__(self, contained_value: Any):
        self._contained_value = contained_value

    def matches(self, value: Any) -> bool:
        try:
            return self._contained_value in value
        except TypeError:
            return False

    def __repr__(self) -> str:
        return f"To contain {repr(self._contained_value)}"

    def concatenated_repr(self) -> str:
        return f"containing {repr(self._contained_value)}"
