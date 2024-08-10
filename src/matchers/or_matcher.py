from typing import Any

from src.matchers import Matcher
from src.utils.repr_utils import concat_reprs


class Or(Matcher):
    def __init__(self, *matchers: Matcher | Any):
        self._matchers = matchers

    def matches(self, value: Any) -> bool:
        return any(matcher == value for matcher in self._matchers)

    def __repr__(self) -> str:
        return concat_reprs("", *self._matchers, separator="or")
