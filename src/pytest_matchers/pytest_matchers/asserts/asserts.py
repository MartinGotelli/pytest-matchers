from typing import Any

from pytest_matchers.asserts.comparer import Comparer


def _match(actual: Any, expected: Any) -> bool:
    return Comparer().compare(actual, expected)


def assert_match(actual: Any, expected: Any) -> None:
    try:
        assert _match(actual, expected)
    except AssertionError:
        assert actual == expected  # Return the original assertion error


def _not_match(actual: Any, expected: Any) -> bool:
    return not _match(actual, expected)


def assert_not_match(actual: Any, expected: Any) -> None:
    try:
        assert _not_match(actual, expected)
    except AssertionError:
        assert actual != expected  # Return the original assertion error
