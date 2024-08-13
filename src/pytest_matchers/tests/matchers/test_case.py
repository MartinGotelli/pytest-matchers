from pytest_matchers import is_number, is_string
from pytest_matchers.matchers import Case


def test_create():
    matcher = Case(3, {3: 3})
    assert isinstance(matcher, Case)
    matcher = Case(3, {3: is_number()})
    assert isinstance(matcher, Case)
    matcher = Case(4, {3: 3}, 3)
    assert isinstance(matcher, Case)
    matcher = Case(3, {3: 3}, 3)
    assert isinstance(matcher, Case)
    matcher = Case(3, {3: 3}, is_string())
    assert isinstance(matcher, Case)


def test_repr():
    matcher = Case(3, {3: 4})
    assert repr(matcher) == "To be 4 because case value is 3"
    matcher = Case(3, {3: is_number()})
    assert repr(matcher) == "To be a number because case value is 3"
    matcher = Case(4, {3: 4}, 5)
    assert repr(matcher) == "To be 5 because case value is 4"
    matcher = Case(4, {3: 3}, is_string())
    assert repr(matcher) == "To be string because case value is 4"
    matcher = Case(4, {3: 3})
    assert (
        repr(matcher) == "To never match because case value 4 is not expected "
        "and the default expectation is not set"
    )


def test_matches():
    matcher = Case(3, {3: 4, 4: "string"})
    assert matcher == 4
    assert matcher != 3
    assert matcher != 5
    assert matcher != "string"
    matcher = Case(3, {3: is_number()})
    assert matcher == 3
    assert matcher == 4
    matcher = Case(3, {3: is_string()}, 3)
    assert matcher == "3"
    assert matcher != 3
    matcher = Case(4, {3: is_number()}, is_string())
    assert matcher == "string"
    assert matcher != 3
    assert matcher != 4
    matcher = Case(4, {3: 3})
    assert matcher != 3
    assert matcher != 4
    assert matcher != "string"
