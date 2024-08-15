from typing import Any

from pytest_matchers.matchers import Matcher


class Eq(Matcher):
    """Why would you want to use this, be serious"""

    def __init__(self, match_value: Any):
        self._match_value = match_value

    def matches(self, value: Any) -> bool:
        return value == self._match_value

    def __repr__(self) -> str:
        return f"To be {repr(self._match_value)}"

    def concatenated_repr(self) -> str:
        return f"equal to {repr(self._match_value)}"
