import pytest

from pytest_matchers.matchers import Length


def test_create():
    matcher = Length()
    assert isinstance(matcher, Length)
    matcher = Length(length=1)
    assert isinstance(matcher, Length)
    matcher = Length(min_length=1, max_length=4)
    assert isinstance(matcher, Length)

    with pytest.raises(
        ValueError,
        match="Cannot specify length with min_length or max_length",
    ):
        Length(length=1, min_length=1)


def test_repr():
    matcher = Length()
    assert repr(matcher) == ""
    matcher = Length(length=1)
    assert repr(matcher) == "To have length of 1"
    matcher = Length(min_length=1, max_length=3)
    assert repr(matcher) == "To have length between 1 and 3"
    matcher = Length(min_length=1)
    assert repr(matcher) == "To have length greater or equal than 1"
    matcher = Length(max_length=3)
    assert repr(matcher) == "To have length lower or equal than 3"


def test_concatenated_repr():
    matcher = Length()
    assert matcher.concatenated_repr() == ""
    matcher = Length(length=1)
    assert matcher.concatenated_repr() == "with length of 1"
    matcher = Length(min_length=1, max_length=3)
    assert matcher.concatenated_repr() == "with length between 1 and 3"
    matcher = Length(min_length=1)
    assert matcher.concatenated_repr() == "with length greater or equal than 1"
    matcher = Length(max_length=3)
    assert matcher.concatenated_repr() == "with length lower or equal than 3"


def test_matches_exact_length():
    matcher = Length(length=1)
    assert matcher.matches([1])
    assert matcher.matches("a")
    assert matcher.matches({"key": "value"})
    assert not matcher.matches([])
    assert not matcher.matches([1, 2])
    assert not matcher.matches("string")


def test_matches_min_and_max_length():
    matcher = Length(min_length=1, max_length=3)
    assert matcher.matches([1])
    assert matcher.matches([1, 2])
    assert matcher.matches([1, 2, 3])
    assert not matcher.matches([])
    assert not matcher.matches([1, 2, 3, 4])


def test_matches_for_value_without_len():
    matcher = Length(min_length=1, max_length=3)
    assert not matcher.matches(1)


def test_matches_without_limits():
    matcher = Length()
    assert matcher.matches([])
    assert matcher.matches([1])
    assert matcher.matches([1, 2])
    assert not matcher.matches(1)
