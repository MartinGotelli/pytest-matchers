from typing import Any, Callable

from pytest_matchers.matchers.base import Matcher
from pytest_matchers.utils.matcher_utils import as_matcher
from pytest_matchers.utils.repr_utils import concat_reprs


class AfterApplying(Matcher):
    def __init__(self, function: Callable, expected_value: Any | Matcher):
        super().__init__()
        self._function = function
        self._expected_value = as_matcher(expected_value)

    def matches(self, value: Any) -> bool:
        try:
            return self._function(value) == self._expected_value
        except Exception:  # pylint: disable=broad-except
            return False

    def __repr__(self):
        return concat_reprs(
            f"After applying the {self._function.__name__} function, the result is expected",
            self._expected_value,
        )
