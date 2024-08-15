from pytest_matchers import is_number, is_string
from pytest_matchers.matchers import JSON


def test_create():
    matcher = JSON()
    assert isinstance(matcher, JSON)
    matcher = JSON({})
    assert isinstance(matcher, JSON)
    matcher = JSON({"key": 4})
    assert isinstance(matcher, JSON)
    matcher = JSON(exclude=["key"])
    assert isinstance(matcher, JSON)
    matcher = JSON({"key": 4}, exclude=["key"])
    assert isinstance(matcher, JSON)


def test_repr():
    matcher = JSON()
    assert repr(matcher) == "To be a JSON"
    matcher = JSON({"key": 4})
    assert repr(matcher) == "To be a JSON expecting 'key' equal to 4"
    matcher = JSON({"key": 4, "other": "string"})
    assert (
        repr(matcher)
        == "To be a JSON expecting 'key' equal to 4 and expecting 'other' equal to 'string'"
    )
    matcher = JSON(exclude=["key"])
    assert repr(matcher) == "To be a JSON excluding 'key'"
    matcher = JSON({"key": 4}, exclude=["other"])
    assert repr(matcher) == "To be a JSON excluding 'other' and expecting 'key' equal to 4"
    matcher = JSON({"string": is_string(), "number": is_number()})
    assert (
        repr(matcher)
        == "To be a JSON expecting 'string' to be a string and expecting 'number' to be a number"
    )


def test_matches():
    matcher = JSON()
    assert matcher == "{}"
    assert matcher == '{"key": 4}'
    assert matcher == '{"key": 4, "other": "string"}'
    assert matcher == '{"key": 4, "other": "string", "extra": 5}'
    assert matcher != "string"
    assert matcher != "{'key': 4}"
    assert matcher != ""
    assert matcher != {"key": 4}
    assert matcher != 3

    matcher = JSON({"key": 4})
    assert matcher == '{"key": 4}'
    assert matcher == '{"key": 4, "other": "string"}'
    assert matcher != '{"key": 5}'
    assert matcher != {"key": 4}

    matcher = JSON(exclude=["key"])
    assert matcher == '{"other": "string"}'
    assert matcher != '{"key": 4}'
    assert matcher != '{"key": 4, "other": "string"}'

    matcher = JSON({"key": 4, "other": "string"}, exclude=["extra"])
    assert matcher == '{"key": 4, "other": "string"}'
    assert matcher != '{"key": 5, "other": "string"}'
    assert matcher != '{"key": 4, "other": "string", "extra": 5}'
    assert matcher != '{"key": 4, "extra": 5}'

    matcher = JSON({"string": is_string(), "number": is_number()})
    assert matcher == '{"string": "string", "number": 3}'
    assert matcher == '{"string": "string", "number": 3, "extra": 5}'
    assert matcher != '{"string": 4, "number": 3}'
    assert matcher != '{"string": "string", "number": "string"}'
    assert matcher != '{"string": "string"}'
