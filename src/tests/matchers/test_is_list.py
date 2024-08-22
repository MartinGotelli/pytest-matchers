# pylint: disable=use-implicit-booleaness-not-comparison
import pytest

from pytest_matchers.matchers import List


def test_create():
    matcher = List(int)
    assert isinstance(matcher, List)

    with pytest.raises(
        ValueError,
        match="Cannot specify length with min_length or max_length",
    ):
        List(int, min_length=1, max_length=4, length=2)


def test_repr():
    matcher = List()
    assert repr(matcher) == "To be a list"
    matcher = List(int)
    assert repr(matcher) == "To be a list of 'int' instance"
    matcher = List(str)
    assert repr(matcher) == "To be a list of 'str' instance"
    matcher = List(int, length=2)
    assert repr(matcher) == "To be a list of 'int' instance and with length of 2"
    matcher = List(int, min_length=2)
    assert repr(matcher) == "To be a list of 'int' instance and with length greater or equal than 2"
    matcher = List(int, max_length=2)
    assert repr(matcher) == "To be a list of 'int' instance and with length lower or equal than 2"
    matcher = List(int, min_length=2, max_length=4)
    assert repr(matcher) == "To be a list of 'int' instance and with length between 2 and 4"
    matcher = List(None, length=2)
    assert repr(matcher) == "To be a list with length of 2"


def test_matches_type():
    assert [] == List(int)
    assert List(int) == []
    assert [1, 2, 3] == List(int)
    assert List(int) == [1, 2, 3]
    assert [1, 2, 3] != List(str)
    assert [1, 2, 3] != List(str)
    assert "string" != List(str)


def test_is_list_without_match_type():
    matcher = List()
    assert matcher == []
    assert matcher == [1]
    assert matcher == ["a"]
    matcher = List(length=2)
    assert matcher == [1, 2]


def test_matches_length():
    matcher = List(int, length=2)
    assert matcher == [1, 2]
    assert matcher != [1]
    assert matcher != [1, 2, 3]


def test_matches_min_length():
    matcher = List(int, min_length=2)
    assert matcher == [1, 2]
    assert matcher == [1, 2, 3]
    assert matcher != [1]
    assert matcher != []


def test_matches_max_length():
    matcher = List(int, max_length=2)
    assert [] == matcher
    assert matcher == []
    assert matcher == [1, 2]
    assert matcher != [1, 2, 3]
    assert matcher != [1, 2, 3, 4]
