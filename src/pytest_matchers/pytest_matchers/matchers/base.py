# pylint: disable=import-outside-toplevel
from abc import ABC, abstractmethod
from typing import Any


class Matcher(ABC):
    def __init__(self):
        self._compared_values = []
        self._compared_values_index = 0

    def __eq__(self, other: Any) -> bool:
        result = self.matches(other)
        if result:
            self._compared_values.append(other)
        return result

    def __and__(self, other: "Matcher") -> "Matcher":
        from pytest_matchers.matchers import And

        return And(self, other)

    def __or__(self, other: "Matcher") -> "Matcher":
        from pytest_matchers.matchers import Or

        return Or(self, other)

    def __invert__(self) -> "Matcher":
        from pytest_matchers.matchers import Not

        return Not(self)

    def __hash__(self):
        return hash(id(self))

    @abstractmethod
    def matches(self, value: Any) -> bool:
        pass

    def concatenated_repr(self) -> str:
        from pytest_matchers.utils.repr_utils import non_capitalized

        return non_capitalized(repr(self))

    def next_compared_value_repr(self) -> str:
        try:
            compare_value = self._compared_values[self._compared_values_index]
            self._compared_values_index += 1
            value = compare_value
            return f"{value!r}"
        except IndexError:
            return repr(self)
