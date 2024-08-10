from typing import Any, Callable

from src.matchers import Between
from src.matchers import Contains
from src.matchers import EndsWith
from src.matchers import Eq, IsInstance, Length, Matcher
from src.matchers import StartsWith


def as_matcher(value: Matcher | Any) -> Matcher:
    if isinstance(value, Matcher):
        return value
    return Eq(value)


def matches_or_none(matcher: Matcher | None, value: Any) -> bool:
    return matcher is None or matcher == value


def partial_matches_or_none(matcher: Matcher | None) -> Callable[[Any], bool]:
    def _partial_matches_or_none(value: Any) -> bool:
        return matches_or_none(matcher, value)

    return _partial_matches_or_none


def is_instance_matcher(match_type: type | None) -> IsInstance | None:
    if match_type is None:
        return None
    return IsInstance(match_type)


def contains_matcher(contains: str | None) -> Contains | None:
    if contains is None:
        return None
    return Contains(contains)


def length_matcher(
    length: int | None,
    max_length: int | None,
    min_length: int | None,
) -> Length | None:
    if length is None and max_length is None and min_length is None:
        return None
    return Length(length, min_length, max_length)


def starts_with_matcher(starts_with: str | None) -> StartsWith | None:
    if starts_with is None:
        return None
    return StartsWith(starts_with)


def ends_with_matcher(ends_with: str | None) -> EndsWith | None:
    if ends_with is None:
        return None
    return EndsWith(ends_with)


def between_matcher(
    min: float | None,
    max: float | None,
    inclusive: bool | None,
    min_inclusive: bool | None,
    max_inclusive: bool | None,
) -> Between | None:
    if min is None and max is None:
        return None
    return Between(
        min,
        max,
        inclusive=inclusive,
        min_inclusive=min_inclusive,
        max_inclusive=max_inclusive,
    )
