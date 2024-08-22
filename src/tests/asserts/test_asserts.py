from typing import Any

import pytest

from pytest_matchers import assert_match, assert_not_match, is_instance
from src.tests.conftest import CustomEqual


def _assert_match_error(actual: Any, expected: Any):
    with pytest.raises(AssertionError):
        assert_match(actual, expected)


def _assert_not_match_error(actual: Any, expected: Any):
    with pytest.raises(AssertionError):
        assert_not_match(actual, expected)


def test_match_eq():
    assert not CustomEqual(3) == is_instance(CustomEqual)  # pylint: disable=unnecessary-negation
    assert not CustomEqual(3) != is_instance(CustomEqual)  # pylint: disable=unnecessary-negation
    assert_match(CustomEqual(3), is_instance(CustomEqual))
    assert_match(is_instance(CustomEqual), CustomEqual(3))
    _assert_match_error(CustomEqual(3), is_instance(str))
    _assert_match_error(is_instance(str), CustomEqual(3))


def test_not_match_eq():
    assert not CustomEqual(3) == is_instance(str)  # pylint: disable=unnecessary-negation
    assert not CustomEqual(3) != is_instance(str)  # pylint: disable=unnecessary-negation
    assert_not_match(CustomEqual(3), is_instance(str))
    assert_not_match(is_instance(str), CustomEqual(3))
    _assert_not_match_error(CustomEqual(3), is_instance(CustomEqual))
    _assert_not_match_error(is_instance(CustomEqual), CustomEqual(3))


def test_match_lists():
    assert_match([CustomEqual(3), 3], [is_instance(CustomEqual), 3])
    assert_not_match([CustomEqual(3), 3], [3, is_instance(CustomEqual)])
    assert_not_match([CustomEqual(3), 3], [is_instance(str), 3])
    assert_not_match([CustomEqual(3), 3], [is_instance(CustomEqual), 4])
    assert_not_match([CustomEqual(3), 3], [is_instance(CustomEqual), 3, 4])


def test_match_sets():
    assert_match({CustomEqual(3), 3}, {is_instance(CustomEqual), 3})
    assert_match({CustomEqual(3), 3}, {3, is_instance(CustomEqual)})
    assert_not_match({CustomEqual(3), 3}, {is_instance(str), 3})
    assert_not_match({CustomEqual(3), 3}, {is_instance(CustomEqual), 4})
    assert_not_match({CustomEqual(3), 3}, {3, is_instance(CustomEqual), 4})


def test_match_tuples():
    assert_match((CustomEqual(3), 3), (is_instance(CustomEqual), 3))
    assert_not_match((CustomEqual(3), 3), (3, is_instance(CustomEqual)))
    assert_not_match((CustomEqual(3), 3), (is_instance(str), 3))
    assert_not_match((CustomEqual(3), 3), (is_instance(CustomEqual), 4))
    assert_not_match((CustomEqual(3), 3), (is_instance(CustomEqual), 3, 4))


def test_match_dictionaries():
    assert_match({"a": CustomEqual(3), "b": 3}, {"a": is_instance(CustomEqual), "b": 3})
    assert_not_match({"a": CustomEqual(3), "b": 3}, {"a": is_instance(str), "b": 3})
    assert_match(
        {"a": CustomEqual(3), "b": [1, 2, CustomEqual(4)]},
        {"a": is_instance(CustomEqual), "b": [1, 2, is_instance(CustomEqual)]},
    )
    assert_match(
        {"a": {"x": CustomEqual(3), "y": 3}, "b": 3},
        {"a": {"x": is_instance(CustomEqual), "y": 3}, "b": 3},
    )
