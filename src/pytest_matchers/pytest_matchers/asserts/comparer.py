from typing import Any

from pytest_matchers.asserts.comparers.dict import DictComparer
from pytest_matchers.asserts.comparers.list import ListComparer
from pytest_matchers.asserts.comparers.set import SetComparer
from pytest_matchers.matchers import Matcher


class Comparer:
    def compare(self, actual: Any, expected: Any, *, fail_fast: bool = True) -> bool:
        if isinstance(expected, Matcher) and not isinstance(actual, Matcher):
            return self.compare(expected, actual, fail_fast=fail_fast)  # Reverse the order
        return self._compare_by_type(actual, expected, fail_fast=fail_fast)

    def _compare_by_type(self, actual: Any, expected: Any, fail_fast: bool = True) -> bool:
        if isinstance(expected, (list, tuple)):
            return ListComparer(actual, expected, fail_fast=fail_fast).compare()
        if isinstance(expected, dict):
            return DictComparer(actual, expected, fail_fast=fail_fast).compare()
        if isinstance(expected, set):
            return SetComparer(actual, expected, fail_fast=fail_fast).compare()
        return actual == expected
