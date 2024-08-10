from typing import Any

from src.matchers import Matcher
from utils.repr_utils import concat_reprs


class And(Matcher):
    def __init__(self, *matchers: Matcher):
        self._matchers = matchers

    def matches(self, value: Any) -> bool:
        return all(matcher == value for matcher in self._matchers)

    def __repr__(self) -> str:
        return concat_reprs("", *self._matchers)
