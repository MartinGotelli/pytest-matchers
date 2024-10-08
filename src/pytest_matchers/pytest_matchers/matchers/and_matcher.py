from typing import Any

from pytest_matchers.matchers import Matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.repr_utils import concat_reprs


@matcher
class And(Matcher):
    def __init__(self, *matchers: Matcher):
        super().__init__()
        self._matchers = matchers

    def matches(self, value: Any) -> bool:
        return all(matcher == value for matcher in self._matchers)

    def __repr__(self) -> str:
        return concat_reprs("", repr(self._matchers[0]), *self._matchers[1:])
