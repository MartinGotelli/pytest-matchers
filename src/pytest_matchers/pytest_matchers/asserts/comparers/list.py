from pytest_matchers.asserts.comparers.base import BaseComparer


class ListComparer(BaseComparer):
    def compare(self) -> bool:
        same_length = len(self._actual) == len(self._expected)
        if not same_length and self._fail_fast:
            return False

        return self._items_compare() and same_length

    def _items_compare(self) -> bool:
        compared_items = (
            self._base_compare(actual_item, expected_item)
            for actual_item, expected_item in zip(self._actual, self._expected)
        )
        if not self._fail_fast:
            compared_items = list(compared_items)  # Force full generation
        return all(compared_items)
