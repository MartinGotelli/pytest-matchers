from typing import Any

from pytest_matchers.matchers import IsInstance, Matcher
from pytest_matchers.utils.matcher_utils import (
    contains_matcher,
    ends_with_matcher,
    length_matcher,
    matches_or_none,
    starts_with_matcher,
)
from pytest_matchers.utils.repr_utils import concat_reprs


class IsString(Matcher):
    def __init__(
        self,
        *,
        starts_with: str = None,
        ends_with: str = None,
        contains: str = None,
        length: int = None,
        max_length: int = None,
        min_length: int = None,
    ):
        self._starts_with_matcher = starts_with_matcher(starts_with)
        self._ends_with_matcher = ends_with_matcher(ends_with)
        self._contains_matcher = contains_matcher(contains)
        self._length_matcher = length_matcher(length, min_length, max_length)

    def matches(self, value: Any) -> bool:
        return (
            IsInstance(str).matches(value)
            and matches_or_none(self._length_matcher, value)
            and matches_or_none(self._contains_matcher, value)
            and matches_or_none(self._starts_with_matcher, value)
            and matches_or_none(self._ends_with_matcher, value)
        )

    def __repr__(self) -> str:
        return concat_reprs(
            "To be a string",
            self._length_matcher,
            self._contains_matcher,
            self._starts_with_matcher,
            self._ends_with_matcher,
        )
