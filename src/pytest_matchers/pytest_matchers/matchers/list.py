from typing import Any, Type

from pytest_matchers.matchers import IsInstance, Matcher
from pytest_matchers.matchers.is_instance import is_instance_matcher
from pytest_matchers.matchers.length import length_matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.matcher_utils import (
    as_matcher_or_none,
    matches_or_none,
    partial_matches_or_none,
)
from pytest_matchers.utils.repr_utils import concat_reprs


@matcher
class List(Matcher):
    def __init__(
        self,
        match_type: Type | Matcher | None = None,
        *,
        length: int | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
    ):
        super().__init__()
        self._type_matcher = (
            is_instance_matcher(match_type)
            if isinstance(match_type, type)
            else as_matcher_or_none(match_type)
        )
        self._length_matcher = length_matcher(length, min_length, max_length)

    def matches(self, value: Any) -> bool:
        return self._matches_type(value) and matches_or_none(self._length_matcher, value)

    def _matches_type(self, value: Any) -> bool:
        return IsInstance(list) == value and all(
            map(partial_matches_or_none(self._type_matcher), value)
        )

    def __repr__(self) -> str:
        return concat_reprs(
            "To be a list",
            self._type_matcher,
            self._length_matcher,
        )

    def concatenated_repr(self):
        return concat_reprs(
            "of lists",
            self._type_matcher,
            self._length_matcher,
        )
