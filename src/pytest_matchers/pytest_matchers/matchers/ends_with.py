from typing import Any, Sized

from pytest_matchers.matchers import Matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.matcher_detector import MatcherDetector
from pytest_matchers.utils.repr_utils import as_matcher_repr


def _ends_with_matcher(prefix: Matcher, value: Any):
    if prefix == value:  # With some luck the matcher matches with the whole value
        return True
    try:
        for index in range(1, len(value)):
            if prefix == value[-index:]:
                return True
    except TypeError:
        pass
    return False


@matcher
class EndsWith(Matcher):
    def __init__(self, suffix: Sized | str | Matcher):
        super().__init__()
        self._suffix = suffix

    def matches(self, value: Any) -> bool:
        if MatcherDetector(self._suffix).uses_matchers():
            return _ends_with_matcher(self._suffix, value)

        if isinstance(value, str):
            try:
                return value.endswith(self._suffix)
            except TypeError:
                return False
        if isinstance(value, list):
            suffix_len = len(self._suffix)
            return value[-suffix_len:] == self._suffix

        return False

    def __repr__(self) -> str:
        return f"To end with {repr(self._suffix)}"

    def concatenated_repr(self) -> str:
        return f"with ending expected {as_matcher_repr(self._suffix)}"


def ends_with_matcher(ends_with: str | None) -> EndsWith | None:
    if ends_with is None:
        return None
    return EndsWith(ends_with)
