from typing import Any

from pytest_matchers.matchers import IsInstance, Matcher
from pytest_matchers.utils.matcher_utils import as_matcher
from pytest_matchers.utils.repr_utils import concat_reprs, non_capitalized


class Dict(Matcher):
    def __init__(self, matching: dict = None, *, exclude: list = None):
        self._is_instance_matcher = IsInstance(dict)
        self._matching = matching or {}
        self._exclude = exclude or []

    def matches(self, value: Any) -> bool:
        return (
            self._is_instance_matcher == value
            and not (set(self._exclude) & set(value.keys()))
            and self._matches_values(value)
        )

    def _matches_values(self, value: dict) -> bool:
        for key, matcher in self._matching.items():
            if key not in value or not matcher == value.get(key):
                return False
        return True

    def __repr__(self):
        return concat_reprs("To be a dictionary", self.expectations_repr())

    def expectations_repr(self):
        exclude_repr = f"excluding {', '.join(map(repr, self._exclude))}" if self._exclude else ""
        matching_reprs = [
            f"expecting {repr(key)} {as_matcher(value).concatenated_repr()}"
            for key, value in self._matching.items()
        ]
        return non_capitalized(concat_reprs("", exclude_repr, *matching_reprs))


def dict_matcher(matching: dict | None, exclude: list | None) -> Dict | None:
    if matching is None and exclude is None:
        return None
    return Dict(matching, exclude=exclude)
