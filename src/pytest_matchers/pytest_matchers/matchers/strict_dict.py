from typing import Any

from pytest_matchers.matchers import IsInstance, Matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.matcher_utils import as_matcher
from pytest_matchers.utils.repr_utils import concat_reprs, non_capitalized


@matcher
class StrictDict(Matcher):
    def __init__(
        self,
        matching: dict,
        *,
        extra_condition: bool = None,
        when_true: dict = None,
        when_false: dict = None,
    ):
        super().__init__()
        self._is_instance_matcher = IsInstance(dict)
        self._matching = matching
        if (when_true or when_false) and extra_condition is None:
            raise ValueError("extra_condition must be set when using when_true or when_false")
        self._extra_condition = extra_condition
        self._when_true = when_true or {}
        self._when_false = when_false or {}

    def matches(self, value: Any) -> bool:
        return self._is_instance_matcher == value and self._expected_dictionary() == value

    def _expected_dictionary(self) -> dict:
        expected_value = self._matching
        if self._extra_condition is not None:
            if self._extra_condition:
                expected_value |= self._when_true
            else:
                expected_value |= self._when_false
        return expected_value

    def __repr__(self) -> str:
        if self._expected_dictionary() == {}:
            return "To be an empty dictionary"
        return concat_reprs("To be a dictionary", self.expectations_repr())

    def expectations_repr(self):
        matching_reprs = [
            f"expecting {repr(key)} {as_matcher(value).concatenated_repr()}"
            for key, value in self._expected_dictionary().items()
        ]
        return non_capitalized(concat_reprs("only", *matching_reprs))
