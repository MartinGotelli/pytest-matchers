from typing import Any

from pytest_matchers.matchers import Matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.matcher_utils import as_matcher


@matcher
class Not(Matcher):
    def __init__(self, value: Matcher | Any):
        super().__init__()
        self._value = as_matcher(value)

    def __new__(cls, value: Matcher | Any):
        if isinstance(value, Not):
            return value._value
        return super().__new__(cls)

    def __invert__(self) -> Matcher:
        return self._value

    def matches(self, value: Any) -> bool:
        return not self._value == value

    def __repr__(self) -> str:
        return f"To not be {self._value.concatenated_repr()}"
