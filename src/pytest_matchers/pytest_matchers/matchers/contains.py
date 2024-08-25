from typing import Any

from pytest_matchers.matchers import Matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.matcher_detector import MatcherDetector
from pytest_matchers.utils.repr_utils import as_matcher_repr


def _in_string_matcher(contained_value: Matcher, value: str):
    if contained_value == value:
        return True
    for i in range(len(value)):
        for j in range(i + 1, len(value) + 1):
            substring = value[i:j]
            if contained_value == substring:
                return True
    return False


@matcher
class Contains(Matcher):
    def __init__(self, *contained_values: Any):
        super().__init__()
        if len(contained_values) == 0:
            raise ValueError("At least one value must be provided")
        self._contained_values = contained_values

    def matches(self, value: Any) -> bool:
        try:
            return all(
                self._in(contained_value, value) for contained_value in self._contained_values
            )
        except TypeError:
            return False

    @staticmethod
    def _in(contained_value: Any, value: Any) -> bool:
        if MatcherDetector(contained_value).uses_matchers() and isinstance(value, str):
            return _in_string_matcher(contained_value, value)
        return contained_value in value

    def __repr__(self) -> str:
        return f"To contain {', '.join(map(repr, self._contained_values))}"

    def concatenated_repr(self) -> str:
        return (
            "containing something expected "
            f"{', and something '.join(map(as_matcher_repr, self._contained_values))}"
        )


def contains_matcher(contains: str | None) -> Contains | None:
    if contains is None:
        return None
    return Contains(contains)
