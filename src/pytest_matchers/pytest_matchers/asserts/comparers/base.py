from abc import ABC, abstractmethod
from typing import Any


class BaseComparer(ABC):
    def __init__(self, actual: Any, expected: Any, *, fail_fast: bool = True):
        self._actual = actual
        self._expected = expected
        self._fail_fast = fail_fast

    @abstractmethod
    def compare(self) -> bool:
        pass

    def _base_compare(self, actual: Any, expected: Any) -> bool:
        # pylint: disable=import-outside-toplevel
        from pytest_matchers.asserts.comparer import Comparer

        return Comparer().compare(actual, expected, fail_fast=self._fail_fast)
