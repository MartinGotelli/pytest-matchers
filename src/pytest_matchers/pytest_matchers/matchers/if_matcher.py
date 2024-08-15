from typing import Any, Callable

from pytest_matchers.matchers import Anything, Matcher
from pytest_matchers.utils.matcher_utils import as_matcher
from pytest_matchers.utils.repr_utils import capitalized
from pytest_matchers.utils.warn import warn


class If(Matcher):
    def __init__(
        self,
        condition: Callable | bool | Any,
        then: Matcher | Any = None,
        or_else: Matcher | Any = None,
    ):
        self._condition = condition
        self._then = as_matcher(then or Anything())
        self._or_else = as_matcher(or_else or Anything())

    def matches(self, value: Any) -> bool:
        matcher = self._or_else
        if self._satisfies_condition(value):
            matcher = self._then
        return matcher == value

    def _satisfies_condition(self, value: Any) -> bool:
        if isinstance(self._condition, bool):
            return self._condition
        if not callable(self._condition):
            return self._condition == value
        try:
            return self._condition(value)
        except Exception as error:  # pylint: disable=broad-except
            warn(f"Condition failed with error: {error}. Returning False as default value.")
            return False

    def __repr__(self):
        if isinstance(self._condition, bool):
            if self._condition:
                return repr(self._then)
            return repr(self._or_else)

        representation = (
            f"{repr(self._then)} if condition returns True"
            f" else {self._or_else.concatenated_repr()}"
        )
        return capitalized(representation)
