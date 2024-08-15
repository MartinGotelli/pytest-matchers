import json
from typing import Any

from pytest_matchers.matchers import IsInstance, Matcher
from pytest_matchers.matchers.dict import dict_matcher
from pytest_matchers.utils.matcher_utils import matches_or_none
from pytest_matchers.utils.repr_utils import concat_reprs


class JSON(Matcher):
    def __init__(self, matching: dict = None, *, exclude: list = None):
        self._is_instance_matcher = IsInstance(str)
        self._dict_matcher = dict_matcher(matching, exclude)

    def matches(self, value: Any) -> bool:
        if self._is_instance_matcher == value:
            try:
                json_data = json.loads(value)
            except json.JSONDecodeError:
                return False
            return matches_or_none(self._dict_matcher, json_data)
        return False

    def __repr__(self) -> str:
        dict_repr = self._dict_matcher.expectations_repr() if self._dict_matcher else ""
        return concat_reprs("To be a JSON", dict_repr)
