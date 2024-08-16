import pytest

from pytest_matchers import is_number, is_string
from pytest_matchers.matchers import StrictDict


def test_create():
    matcher = StrictDict({})
    assert isinstance(matcher, StrictDict)
    matcher = StrictDict({"a": "b"})
    assert isinstance(matcher, StrictDict)
    matcher = StrictDict({}, extra_condition=True, when_true={"a": 1}, when_false={"b": 2})
    assert isinstance(matcher, StrictDict)
    matcher = StrictDict({}, extra_condition=False, when_true={"a": 1})
    assert isinstance(matcher, StrictDict)
    matcher = StrictDict({}, extra_condition=False, when_false={"b": 2})
    assert isinstance(matcher, StrictDict)
    with pytest.raises(
        ValueError,
        match="extra_condition must be set when using when_true or when_false",
    ):
        StrictDict({}, when_true={"a": 1})


def test_repr():
    matcher = StrictDict({})
    assert repr(matcher) == "To be an empty dictionary"
    matcher = StrictDict({"a": "b"})
    assert repr(matcher) == "To be a dictionary only expecting 'a' equal to 'b'"
    matcher = StrictDict({}, extra_condition=True, when_true={"a": 1}, when_false={"b": 2})
    assert repr(matcher) == "To be a dictionary only expecting 'a' equal to 1"
    matcher = StrictDict({}, extra_condition=False, when_true={"a": 1})
    assert repr(matcher) == "To be an empty dictionary"
    matcher = StrictDict({}, extra_condition=False, when_false={"b": 2})
    assert repr(matcher) == "To be a dictionary only expecting 'b' equal to 2"
    matcher = StrictDict({"x": 3, 2: True}, extra_condition=True, when_true={"a": 1})
    assert (
        repr(matcher) == "To be a dictionary only expecting 'x' equal to 3 and "
        "expecting 2 equal to True and expecting 'a' equal to 1"
    )


def test_matches():
    matcher = StrictDict({})
    assert matcher == {}  # pylint: disable=use-implicit-booleaness-not-comparison
    assert matcher != {"a": 1}
    assert matcher != 9
    matcher = StrictDict({"a": 1})
    assert matcher == {"a": 1}
    assert matcher != {"a": 2}
    assert matcher != {"b": 1}
    matcher = StrictDict({"a": 1, "b": 2})
    assert matcher == {"a": 1, "b": 2}
    assert matcher != {"a": 2, "b": 1}
    assert matcher != {"a": 1}
    assert matcher != {"b": 2}
    matcher = StrictDict({"a": 1}, extra_condition=True, when_true={"b": 2})
    assert matcher == {"a": 1, "b": 2}
    assert matcher != {"a": 1}
    assert matcher != {"b": 2}
    assert matcher != {"a": 1, "b": 1}
    matcher = StrictDict({"a": 1}, extra_condition=False, when_true={"c": 3}, when_false={"b": 2})
    assert matcher == {"a": 1, "b": 2}
    assert matcher != {"a": 1}
    assert matcher != {"a": 1, "c": 3}
    matcher = StrictDict(
        {"a": 1, "b": 2},
        extra_condition=True,
        when_true={"c": 3},
        when_false={"b": 2},
    )
    assert matcher == {"a": 1, "b": 2, "c": 3}
    assert matcher != {"a": 1, "b": 2}
    assert matcher != {"a": 1, "c": 3}
    assert matcher != {"b": 2, "c": 3}
    matcher = StrictDict({"a": 1, "b": 2}, extra_condition=False, when_true={"c": 3})
    assert matcher == {"a": 1, "b": 2}
    assert matcher != {"a": 1, "b": 2, "c": 3}
    matcher = StrictDict(
        {"a": 1},
        extra_condition=True,
        when_true={"b": is_string()},
        when_false={"b": is_number()},
    )
    assert matcher == {"a": 1, "b": "string"}
    assert matcher != {"a": 1, "b": 2}
