from pytest_matchers import is_number, is_string
from pytest_matchers.matchers import If


def test_create():
    matcher = If(True)
    assert isinstance(matcher, If)
    matcher = If(False)
    assert isinstance(matcher, If)
    matcher = If(lambda x: x == 3)
    assert isinstance(matcher, If)
    matcher = If(lambda x: x == 3, 3)
    assert isinstance(matcher, If)
    matcher = If(lambda x: x == 3, 3, 4)
    assert isinstance(matcher, If)
    matcher = If(lambda x: x == 3, or_else=4)
    assert isinstance(matcher, If)


def test_repr():
    matcher = If(True)
    assert repr(matcher) == "To be anything"
    matcher = If(False, is_string(), is_number(int))
    assert repr(matcher) == "To be a number of 'int' instance"
    matcher = If(lambda x: x == 3)
    assert repr(matcher) == "To be anything if condition returns True else to be anything"
    matcher = If(lambda x: x == 3, 3)
    assert repr(matcher) == "To be 3 if condition returns True else to be anything"
    matcher = If(lambda x: x == 3, is_number(), 4)
    assert repr(matcher) == "To be a number if condition returns True else to be 4"
    matcher = If(lambda x: x == 3, or_else=is_string())
    assert repr(matcher) == "To be anything if condition returns True else to be string"


def test_match():
    assert If(True) == 3
    assert If(False) == 3
    matcher = If(True, is_number(), is_string())
    assert matcher == 3
    assert matcher == 4
    assert matcher != "string"
    matcher = If(False, is_number(), is_string())
    assert matcher != 3
    assert matcher != 4
    assert matcher == "string"
    matcher = If(lambda x: x > 3, is_number(float), is_number(int))
    assert matcher == 3
    assert matcher != 4
    matcher = If(lambda x: x + 2 == 5, 3)
    assert matcher == 3
    assert matcher == 4  # False can be anything
    assert matcher == "string"
    matcher = If(lambda x: x <= 3, 3, 4)
    assert matcher == 3
    assert matcher == 4
    assert matcher != "string"
    matcher = If(lambda x: x + 2 == 5, or_else=4)
    assert matcher == 3
    assert matcher == 4
    assert matcher != "string"
    matcher = If(5, is_number(), is_string())
    assert matcher == 5
    assert matcher != 4
    assert matcher == "string"
    matcher = If(is_string(), is_string(length=8), is_number())
    assert matcher == "string__"
    assert matcher != "string"
    assert matcher == 3
    assert matcher != [1]
