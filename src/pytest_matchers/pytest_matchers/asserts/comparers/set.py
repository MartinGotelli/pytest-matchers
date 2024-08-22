from typing import Any, Set

from pytest_matchers.asserts.comparers.base import BaseComparer


class SetComparer(BaseComparer):
    def compare(self) -> bool:
        same_length = len(self._actual) == len(self._expected)
        if not same_length and self._fail_fast:
            return False

        return self._items_compare() and same_length

    def _items_compare(self) -> bool:
        expected = self._expected.copy()
        compared_items = (self._in(actual_value, expected) for actual_value in self._actual)
        if not self._fail_fast:
            compared_items = list(compared_items)
        return all(compared_items) and not expected

    def _in(self, actual_value: Any, expected: Set[Any]) -> bool:
        for expected_value in expected:
            if self._base_compare(actual_value, expected_value):
                expected.discard(expected_value)
                return True
        return False
