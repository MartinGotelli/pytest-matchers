from typing import Any

from pytest_matchers.matchers import Matcher
from pytest_matchers.utils.matcher_utils import as_matcher, matches_or_none


class HasAttribute(Matcher):
    def __init__(self, attribute_name: str, expected_value: Any = None):
        self._attribute_name = attribute_name
        self._expected_value = expected_value
        self._expected_value_matcher = as_matcher(expected_value) if expected_value else None

    def matches(self, value: Any) -> bool:
        return hasattr(value, self._attribute_name) and matches_or_none(
            self._expected_value_matcher,
            getattr(value, self._attribute_name),
        )

    def __repr__(self) -> str:
        base_repr = f"To have attribute {repr(self._attribute_name)}"
        if self._expected_value_matcher:
            return f"{base_repr} and {self._expected_value_matcher.concatenated_repr()}"
        return base_repr

    def concatenated_repr(self) -> str:
        base_repr = f"with {repr(self._attribute_name)}"
        if self._expected_value:
            if isinstance(self._expected_value, Matcher):
                return f"{base_repr} expecting {self._expected_value.concatenated_repr()}"
            return f"{base_repr} being {repr(self._expected_value)}"
        return base_repr


def has_attribute_matcher(
    attribute: str | None,
    value: Any,
    value_needed: bool = False,
) -> HasAttribute | None:
    if not attribute:
        return None
    if value_needed and value is None:
        return None
    return HasAttribute(attribute, value)
