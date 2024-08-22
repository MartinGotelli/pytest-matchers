import uuid
from typing import Any, Type

from pytest_matchers.matchers import Matcher
from pytest_matchers.matchers.matcher_factory import matcher
from pytest_matchers.utils.matcher_utils import (
    as_matcher_or_none,
    is_instance_matcher,
    matches_or_none,
)
from pytest_matchers.utils.repr_utils import concat_matcher_repr, concat_reprs


@matcher
class UUID(Matcher):
    def __init__(self, matching_type: Type = None, *, version: int | Matcher = None):
        super().__init__()
        self._is_instance_matcher = is_instance_matcher(matching_type)
        self._version_matcher = as_matcher_or_none(version)

    def matches(self, value: Any) -> bool:
        if matches_or_none(self._is_instance_matcher, value):
            try:
                uuid_value = uuid.UUID(str(value))
                return matches_or_none(self._version_matcher, uuid_value.version)
            except ValueError:
                pass
        return False

    def __repr__(self) -> str:
        base_repr = "To be a UUID"
        instance_matcher_repr = concat_matcher_repr(self._is_instance_matcher) or ""
        version_matcher_repr = (
            f"with version {concat_matcher_repr(self._version_matcher)}"
            if self._version_matcher
            else ""
        )
        return concat_reprs(f"{base_repr}", instance_matcher_repr, version_matcher_repr)
