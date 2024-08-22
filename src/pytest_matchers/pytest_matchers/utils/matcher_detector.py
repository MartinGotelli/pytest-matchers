from typing import Any

from pytest_matchers.matchers import Matcher


class MatcherDetector:
    def __init__(self, value: Any):
        self._value = value

    def uses_matchers(self) -> bool:
        return isinstance(self._value, Matcher) or self._iterable_with_matchers()

    def _iterable_with_matchers(self) -> bool:
        if isinstance(self._value, dict):
            return any(MatcherDetector(value).uses_matchers() for value in self._value.values())
        if isinstance(self._value, (list, tuple, set)):
            return any(MatcherDetector(value).uses_matchers() for value in self._value)
        return False
