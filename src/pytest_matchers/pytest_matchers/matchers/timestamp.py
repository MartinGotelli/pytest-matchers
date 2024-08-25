from datetime import datetime
from typing import Any

from pytest_matchers.matchers import Matcher, Number
from pytest_matchers.matchers.between import between_matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.matcher_utils import matches_or_none
from pytest_matchers.utils.repr_utils import concat_reprs


def _as_timestamp(value: float | datetime) -> float:
    if isinstance(value, datetime):
        return value.timestamp()
    return value


@matcher
class Timestamp(Matcher):
    def __init__(self, *, min_value: float | datetime = None, max_value: float | datetime = None):
        super().__init__()
        self._instance_matcher = Number()
        self._limit_matcher = between_matcher(
            _as_timestamp(min_value),
            _as_timestamp(max_value),
            None,
            None,
            None,
        )

    def matches(self, value: Any) -> bool:
        return self._instance_matcher == value and matches_or_none(self._limit_matcher, value)

    def __repr__(self) -> str:
        return concat_reprs("To be a timestamp", self._limit_matcher)
