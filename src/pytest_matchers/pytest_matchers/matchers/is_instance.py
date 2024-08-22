from typing import Any

from pytest_matchers.matchers import Matcher
from pytest_matchers.matchers.matcher_factory import matcher


@matcher
class IsInstance(Matcher):
    def __init__(self, match_type):
        super().__init__()
        self._match_type = match_type

    def matches(self, value: Any) -> bool:
        return isinstance(value, self._match_type)

    def __repr__(self) -> str:
        return f"To be instance of '{self._match_type.__name__}'"

    def concatenated_repr(self) -> str:
        return f"of '{self._match_type.__name__}' instance"
