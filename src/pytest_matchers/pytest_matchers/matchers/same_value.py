from typing import Any

from pytest_matchers.matchers import Matcher


class SameValue(Matcher):
    def __init__(self):
        self._matched_value = None

    def matches(self, value: Any) -> bool:
        if self._matched_value is None:
            self._matched_value = value
            return True
        return self._matched_value == value

    def __repr__(self) -> str:
        if self._matched_value is None:
            return "To be the same value"
        return f"To be the same value as {repr(self._matched_value)}"
