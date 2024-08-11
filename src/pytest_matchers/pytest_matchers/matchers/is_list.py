from typing import Any, Callable, Type

from pytest_matchers.matchers import IsInstance, Matcher
from pytest_matchers.utils.matcher_utils import (
    is_instance_matcher,
    length_matcher,
    matches_or_none,
    partial_matches_or_none,
)
from pytest_matchers.utils.repr_utils import concat_reprs


class IsList(Matcher):
    def __init__(
        self,
        match_type: Type = None,
        *,
        length: int = None,
        min_length: int = None,
        max_length: int = None,
    ):
        self._is_instance_matcher = is_instance_matcher(match_type)
        self._length_matcher = length_matcher(length, min_length, max_length)

    def matches(self, value: Any) -> bool:
        return self._matches_type(value) and matches_or_none(self._length_matcher, value)

    def _matches_type(self, value: Any) -> bool:
        return IsInstance(list) == value and all(map(self._type_matcher(), value))

    def _type_matcher(self) -> Callable[[Any], bool]:
        return partial_matches_or_none(self._is_instance_matcher)

    def __repr__(self) -> str:
        return concat_reprs(
            "To be a list",
            self._is_instance_matcher,
            self._length_matcher,
        )
