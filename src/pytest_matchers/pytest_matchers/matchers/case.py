from typing import Any

from pytest_matchers.matchers import Matcher
from pytest_matchers.utils.matcher_utils import as_matcher, as_matcher_or_none


class Case(Matcher):
    def __init__(
        self,
        case_value: Any,
        expectations: dict[Any, Matcher | Any],
        default_expectation: Matcher | Any | None = None,
    ):
        self._case_value = case_value
        self._expectations = expectations
        self._default_expectation = (
            None if default_expectation is None else as_matcher(default_expectation)
        )

    def matches(self, value: Any) -> bool:
        expectation = self._expectation()
        if expectation is None:
            return False
        return value == expectation

    def _expectation(self) -> Matcher | Any | None:
        return as_matcher_or_none(
            self._expectations.get(self._case_value, self._default_expectation)
        )

    def __repr__(self):
        expectation = self._expectation()
        if expectation is None:
            return (
                f"To never match because case value {repr(self._case_value)} is not expected "
                "and the default expectation is not set"
            )
        return f"{repr(expectation)} because case value is {repr(self._case_value)}"
