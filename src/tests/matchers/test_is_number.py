import pytest

from pytest_matchers.matchers import Number


def test_create():
    matcher = Number()
    assert isinstance(matcher, Number)
    matcher = Number(int)
    assert isinstance(matcher, Number)
    matcher = Number(min_value=1, max_value=2)
    assert isinstance(matcher, Number)
    matcher = Number(min_value=1, max_value=2, min_inclusive=False)
    assert isinstance(matcher, Number)
    with pytest.raises(
        ValueError,
        match="Cannot specify inclusive and min_inclusive or max_inclusive",
    ):
        Number(min_value=1, max_value=2, inclusive=True, min_inclusive=True)


def test_repr():
    matcher = Number()
    assert repr(matcher) == "To be a number"
    matcher = Number(int)
    assert repr(matcher) == "To be a number of 'int' instance"
    matcher = Number(min_value=1, max_value=2)
    assert repr(matcher) == "To be a number between 1 and 2"
    matcher = Number(min_value=1, max_value=2, inclusive=False)
    assert repr(matcher) == "To be a number between 1 and 2 exclusive"
    matcher = Number(min_value=1, max_value=2, min_inclusive=False)
    assert repr(matcher) == "To be a number greater than 1 and lower or equal than 2"
    matcher = Number(min_value=1, max_value=2, max_inclusive=False)
    assert repr(matcher) == "To be a number greater or equal than 1 and lower than 2"
    matcher = Number(float, min_value=1, max_value=2)
    assert repr(matcher) == "To be a number of 'float' instance and between 1 and 2"
    matcher = Number(min_value=1, max_value=1)
    assert repr(matcher) == "To be a number equal to 1"


def test_matches_number():
    matcher = Number()
    assert matcher == 20
    assert matcher == 20.0
    assert matcher != "string"
    assert matcher != ["string"]


def test_matches_type():
    matcher = Number(int)
    assert matcher == 20
    assert matcher != 20.0
    assert matcher != "string"
    assert matcher != ["string"]


def test_matches_limit_inclusive():
    matcher = Number(min_value=1, max_value=2)
    assert matcher == 1
    assert matcher == 1.5
    assert matcher == 2
    assert matcher != 0
    assert matcher != 3
    assert matcher != "string"


def test_matches_limit_exclusive():
    matcher = Number(min_value=1, max_value=2, inclusive=False)
    assert matcher == 1.5
    assert matcher != 1
    assert matcher != 2
    assert matcher != 0
    assert matcher != 3
    assert matcher != "string"


def test_matches_min_exclusive():
    matcher = Number(min_value=1, max_value=2, min_inclusive=False)
    assert matcher == 1.5
    assert matcher == 2
    assert matcher != 1
    assert matcher != 0
    assert matcher != 3
    assert matcher != "string"


def test_matches_max_exclusive():
    matcher = Number(min_value=1, max_value=2, max_inclusive=False)
    assert matcher == 1
    assert matcher == 1.5
    assert matcher != 2
    assert matcher != 0
    assert matcher != 3
    assert matcher != "string"


def test_matches_without_max():
    matcher = Number(min_value=1)
    assert matcher == 1
    assert matcher == 1.5
    assert matcher == 3
    assert matcher != 0.99
    assert matcher != "string"
    assert matcher != ["string"]
    assert matcher != [1, 2]
