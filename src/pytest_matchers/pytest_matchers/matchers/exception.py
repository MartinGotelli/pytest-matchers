from builtins import Exception

from pytest_matchers.matchers.base import Matcher
from pytest_matchers.utils.matcher_utils import as_matcher_or_none, matches_or_none
from pytest_matchers.utils.repr_utils import concat_matcher_repr


class ExceptionMatcher(Matcher):
    def __init__(
        self,
        exception_type: type[Exception] = Exception,
        message: str | Matcher | None = None,
        match_subclass: bool = False,
    ):
        super().__init__()
        self._exception_type = exception_type
        self._message_matcher = as_matcher_or_none(message)
        self._match_subclass = match_subclass

    def matches(self, value: Exception) -> bool:
        return self._matches_type(value) and self._matches_message(value)

    def __repr__(self) -> str:
        representation = "To be an exception"
        if self._match_subclass:
            representation += " instance of"
        else:
            representation += " of type"
        representation += f" {self._exception_type.__name__}"
        if self._message_matcher:
            representation += f" with message expected {concat_matcher_repr(self._message_matcher)}"
        return representation

    def _matches_type(self, value: Exception) -> bool:
        if self._match_subclass:
            return isinstance(value, self._exception_type)
        return type(value) == self._exception_type  # pylint: disable=unidiomatic-typecheck

    def _matches_message(self, value: Exception) -> bool:
        return matches_or_none(self._message_matcher, str(value))
