from typing import Any

from pytest_matchers.matchers import Matcher
from pytest_matchers.utils.matcher_utils import as_matcher


class Not(Matcher):
    def __init__(self, matcher: Matcher | Any):
        self._matcher = as_matcher(matcher)

    def __new__(cls, matcher):
        if isinstance(matcher, Not):
            return matcher._matcher
        return super().__new__(cls)

    def __invert__(self) -> Matcher:
        return self._matcher

    def matches(self, value) -> bool:
        return not self._matcher == value

    def __repr__(self) -> str:
        return f"To not be {self._matcher.concatenated_repr()}"
