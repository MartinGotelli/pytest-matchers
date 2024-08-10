# pylint: disable=use-implicit-booleaness-not-comparison
import pytest

from pytest_matchers.matchers import IsList


def test_create():
    matcher = IsList(int)
    assert isinstance(matcher, IsList)

    with pytest.raises(
        ValueError,
        match="Cannot specify length with min_length or max_length",
    ):
        IsList(int, min_length=1, max_length=4, length=2)


def test_repr():
    matcher = IsList()
    assert repr(matcher) == "To be a list"
    matcher = IsList(int)
    assert repr(matcher) == "To be a list of 'int' instance"
    matcher = IsList(str)
    assert repr(matcher) == "To be a list of 'str' instance"
    matcher = IsList(int, length=2)
    assert repr(matcher) == "To be a list of 'int' instance and with length of 2"
    matcher = IsList(int, min_length=2)
    assert repr(matcher) == "To be a list of 'int' instance and with length greater or equal than 2"
    matcher = IsList(int, max_length=2)
    assert repr(matcher) == "To be a list of 'int' instance and with length lower or equal than 2"
    matcher = IsList(int, min_length=2, max_length=4)
    assert repr(matcher) == "To be a list of 'int' instance and with length between 2 and 4"
    matcher = IsList(None, length=2)
    assert repr(matcher) == "To be a list with length of 2"


def test_matches_type():
    assert [] == IsList(int)
    assert IsList(int) == []
    assert [1, 2, 3] == IsList(int)
    assert IsList(int) == [1, 2, 3]
    assert [1, 2, 3] != IsList(str)
    assert [1, 2, 3] != IsList(str)
    assert "string" != IsList(str)


def test_is_list_without_match_type():
    matcher = IsList()
    assert matcher == []
    assert matcher == [1]
    assert matcher == ["a"]
    matcher = IsList(length=2)
    assert matcher == [1, 2]


def test_matches_length():
    matcher = IsList(int, length=2)
    assert matcher == [1, 2]
    assert matcher != [1]
    assert matcher != [1, 2, 3]


def test_matches_min_length():
    matcher = IsList(int, min_length=2)
    assert matcher == [1, 2]
    assert matcher == [1, 2, 3]
    assert matcher != [1]
    assert matcher != []


def test_matches_max_length():
    matcher = IsList(int, max_length=2)
    assert [] == matcher
    assert matcher == []
    assert matcher == [1, 2]
    assert matcher != [1, 2, 3]
    assert matcher != [1, 2, 3, 4]
