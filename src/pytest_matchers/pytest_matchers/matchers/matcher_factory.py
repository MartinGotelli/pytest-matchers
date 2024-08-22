from typing import IO

from _pytest._io.pprint import PrettyPrinter

from pytest_matchers.matchers import Matcher


def _print_matcher(
    _printer: PrettyPrinter,
    matcher_instance: Matcher,
    stream: IO[str],
    _indent: int,
    _allowance: int,
    _context: set[int],
    _level: int,
):
    stream.write(matcher_instance.next_compared_value_repr())


class MatcherFactory:
    matchers = {}

    @classmethod
    def register(cls, matcher_class: Matcher):
        PrettyPrinter._dispatch[matcher_class.__repr__] = (  # pylint: disable=protected-access
            _print_matcher
        )
        cls.matchers[matcher_class.__name__] = matcher_class

    @classmethod
    def get(cls, name):
        return cls.matchers[name]


def matcher(matcher_class):
    MatcherFactory.register(matcher_class)
    return matcher_class
