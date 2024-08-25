from typing import Any, Callable

from pytest_matchers.matchers import Eq, Matcher


def as_matcher(value: Matcher | Any) -> Matcher:
    if isinstance(value, Matcher):
        return value
    return Eq(value)


def as_matcher_or_none(value: Matcher | Any | None) -> Matcher | None:
    if value is None:
        return None
    return as_matcher(value)


def matches_or_none(matcher: Matcher | None, value: Any) -> bool:
    return matcher is None or matcher == value


def partial_matches_or_none(matcher: Matcher | None) -> Callable[[Any], bool]:
    def _partial_matches_or_none(value: Any) -> bool:
        return matches_or_none(matcher, value)

    return _partial_matches_or_none
