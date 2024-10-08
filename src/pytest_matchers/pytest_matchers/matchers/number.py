from typing import Any, Type

from pytest_matchers.matchers import Matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.matcher_utils import (
    matches_or_none,
)
from pytest_matchers.matchers.is_instance import is_instance_matcher
from pytest_matchers.matchers.between import between_matcher
from pytest_matchers.utils.repr_utils import concat_reprs


@matcher
class Number(Matcher):
    def __init__(
        self,
        match_type: Type = None,
        *,
        min_value: float = None,
        max_value: float = None,
        inclusive: bool = None,
        min_inclusive: bool = None,
        max_inclusive: bool = None,
    ):
        super().__init__()
        self._is_instance_matcher = is_instance_matcher(match_type)
        self._between_matcher = between_matcher(
            min_value,
            max_value,
            inclusive,
            min_inclusive,
            max_inclusive,
        )

    def matches(self, value: Any) -> bool:
        return self._matches_type(value) and self._matches_limit(value)

    def _matches_type(self, value: Any) -> bool:
        if self._is_instance_matcher is None:
            try:
                float(value)
                return True
            except (ValueError, TypeError):
                return False
        return self._is_instance_matcher == value

    def _matches_limit(self, value: Any) -> bool:
        return matches_or_none(self._between_matcher, value)

    def __repr__(self) -> str:
        return concat_reprs(
            "To be a number",
            self._is_instance_matcher,
            self._between_matcher,
        )
