# pylint: disable=import-outside-toplevel
from abc import ABC, abstractmethod
from typing import Any


class Matcher(ABC):
    def __eq__(self, other: Any) -> bool:
        return self.matches(other)

    def __and__(self, other: "Matcher") -> "Matcher":
        from pytest_matchers.matchers import And

        return And(self, other)

    def __or__(self, other: "Matcher") -> "Matcher":
        from pytest_matchers.matchers import Or

        return Or(self, other)

    def __invert__(self) -> "Matcher":
        from pytest_matchers.matchers import Not

        return Not(self)

    @abstractmethod
    def matches(self, value: Any) -> bool:
        pass

    def concatenated_repr(self) -> str:
        from pytest_matchers.utils.repr_utils import non_capitalized

        return non_capitalized(repr(self))
