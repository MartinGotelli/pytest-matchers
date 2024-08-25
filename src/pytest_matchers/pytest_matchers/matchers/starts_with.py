from typing import Any, Sized

from pytest_matchers.matchers import Matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.matcher_detector import MatcherDetector
from pytest_matchers.utils.repr_utils import as_matcher_repr


def _starts_with_matcher(prefix: Matcher, value: Any):
    if prefix == value:  # With some luck the matcher matches with the whole value
        return True
    try:
        for index in range(1, len(value)):
            if prefix == value[0:index]:
                return True
    except TypeError:
        pass
    return False


@matcher
class StartsWith(Matcher):
    def __init__(self, prefix: Sized | str | Matcher):
        super().__init__()
        self._prefix = prefix

    def matches(self, value: Any) -> bool:
        if MatcherDetector(self._prefix).uses_matchers():
            return _starts_with_matcher(self._prefix, value)

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
        return f"with start expected {as_matcher_repr(self._prefix)}"


def starts_with_matcher(starts_with: str | None) -> StartsWith | None:
    if starts_with is None:
        return None
    return StartsWith(starts_with)
