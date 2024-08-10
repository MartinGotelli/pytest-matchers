import pytest

from src.matchers import IsNumber


def test_create():
    matcher = IsNumber()
    assert isinstance(matcher, IsNumber)
    matcher = IsNumber(int)
    assert isinstance(matcher, IsNumber)
    matcher = IsNumber(min=1, max=2)
    assert isinstance(matcher, IsNumber)
    matcher = IsNumber(min=1, max=2, min_inclusive=False)
    assert isinstance(matcher, IsNumber)
    with pytest.raises(
        ValueError,
        match="Cannot specify inclusive and min_inclusive or max_inclusive",
    ):
        IsNumber(min=1, max=2, inclusive=True, min_inclusive=True)


def test_repr():
    matcher = IsNumber()
    assert repr(matcher) == "To be a number"
    matcher = IsNumber(int)
    assert repr(matcher) == "To be a number of 'int' instance"
    matcher = IsNumber(min=1, max=2)
    assert repr(matcher) == "To be a number between 1 and 2"
    matcher = IsNumber(min=1, max=2, inclusive=False)
    assert repr(matcher) == "To be a number between 1 and 2 exclusive"
    matcher = IsNumber(min=1, max=2, min_inclusive=False)
    assert repr(matcher) == "To be a number greater than 1 and lower or equal than 2"
    matcher = IsNumber(min=1, max=2, max_inclusive=False)
    assert repr(matcher) == "To be a number greater or equal than 1 and lower than 2"
    matcher = IsNumber(float, min=1, max=2)
    assert repr(matcher) == "To be a number of 'float' instance and between 1 and 2"


def test_matches_number():
    matcher = IsNumber()
    assert matcher == 20
    assert matcher == 20.0
    assert matcher != "string"
    assert matcher != ["string"]


def test_matches_type():
    matcher = IsNumber(int)
    assert matcher == 20
    assert matcher != 20.0
    assert matcher != "string"
    assert matcher != ["string"]


def test_matches_limit_inclusive():
    matcher = IsNumber(min=1, max=2)
    assert matcher == 1
    assert matcher == 1.5
    assert matcher == 2
    assert not matcher == 0
    assert not matcher == 3
    assert not matcher == "string"


def test_matches_limit_exclusive():
    matcher = IsNumber(min=1, max=2, inclusive=False)
    assert matcher == 1.5
    assert not matcher == 1
    assert not matcher == 2
    assert not matcher == 0
    assert not matcher == 3
    assert not matcher == "string"


def test_matches_min_exclusive():
    matcher = IsNumber(min=1, max=2, min_inclusive=False)
    assert matcher == 1.5
    assert matcher == 2
    assert not matcher == 1
    assert not matcher == 0
    assert not matcher == 3
    assert not matcher == "string"


def test_matches_max_exclusive():
    matcher = IsNumber(min=1, max=2, max_inclusive=False)
    assert matcher == 1
    assert matcher == 1.5
    assert not matcher == 2
    assert not matcher == 0
    assert not matcher == 3
    assert not matcher == "string"


def test_matches_without_max():
    matcher = IsNumber(min=1)
    assert matcher == 1
    assert matcher == 1.5
    assert matcher == 3
    assert matcher != 0.99
    assert matcher != "string"
    assert matcher != ["string"]
    assert matcher != [1, 2]
