from typing import Any

import pytest

from pytest_matchers.matchers import Matcher
from pytest_matchers.utils.matcher_detector import MatcherDetector


def _matches_operation(operation, actual: Any, expected: Matcher) -> bool:
    if operation == "==":
        return expected == actual
    if operation == "!=":
        return expected != actual
    return False  # pragma: no cover


@pytest.hookimpl()
def pytest_assertrepr_compare(config, op: str, left: Any, right: Any):
    del config
    if (
        MatcherDetector(left).uses_matchers()
        or MatcherDetector(right).uses_matchers()
        and _matches_operation(op, left, right)
    ):
        return [
            f"{left!r} {op} {right!r}",
            "",
            "WARNING! "
            "Comparison failed because the left object redefines the equality operator.",
            "Consider using the 'assert_match' or 'assert_not_match' functions instead.",
            "assert_match(actual, expected)",
        ]
    return None
