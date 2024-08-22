from typing import Generator

from pytest_matchers.asserts.comparers.base import BaseComparer


class DictComparer(BaseComparer):
    def compare(self) -> bool:
        same_length = len(self._actual) == len(self._expected)
        if not same_length and self._fail_fast:
            return False

        return self._items_compare() and same_length

    def _items_compare(self) -> bool:
        compared_items = self._compared_items()
        if not self._fail_fast:
            compared_items = list(compared_items)
        return all(compared_items)

    def _compared_items(self) -> Generator:
        for key in self._expected:
            if key in self._actual:
                yield self._base_compare(self._actual[key], self._expected[key])
            else:
                yield False
