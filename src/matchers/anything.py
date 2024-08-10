from typing import Any

from src.matchers import Matcher


class Anything(Matcher):
    def matches(self, _value: Any) -> bool:
        return True

    def __repr__(self) -> str:
        return "To be anything"
