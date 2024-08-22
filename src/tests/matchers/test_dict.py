from pytest_matchers import anything, is_number, is_string
from pytest_matchers.matchers import Dict


def test_create():
    matcher = Dict()
    assert isinstance(matcher, Dict)
    matcher = Dict({"key": 3})
    assert isinstance(matcher, Dict)
    matcher = Dict({"key": 3}, exclude=["other"])
    assert isinstance(matcher, Dict)


def test_repr():
    matcher = Dict()
    assert repr(matcher) == "To be a dictionary"
    matcher = Dict({"key": 3})
    assert repr(matcher) == "To be a dictionary expecting 'key' equal to 3"
    matcher = Dict({"key": 3, "other": "string"})
    assert (
        repr(matcher)
        == "To be a dictionary expecting 'key' equal to 3 and expecting 'other' equal to 'string'"
    )
    matcher = Dict(exclude=["key"])
    assert repr(matcher) == "To be a dictionary excluding 'key'"
    matcher = Dict({"key": 3}, exclude=["other"])
    assert repr(matcher) == "To be a dictionary excluding 'other' and expecting 'key' equal to 3"
    matcher = Dict({"key": is_string(), "any": anything(), "other": 3})
    assert (
        repr(matcher) == "To be a dictionary expecting 'key' to be a string and "
        "expecting 'any' to be anything and expecting 'other' equal to 3"
    )


def test_matches():
    matcher = Dict()
    assert matcher == {}  # pylint: disable=use-implicit-booleaness-not-comparison
    assert matcher == {"key": 3}
    assert matcher != [1, 2, 3]
    assert matcher != "string"
    matcher = Dict({"key": 3})
    assert matcher == {"key": 3}
    assert matcher == {"key": 3, "other": 4}
    assert matcher != {"key": 4}
    assert matcher != {"other": 3}
    matcher = Dict({"key": 3}, exclude=["other"])
    assert matcher == {"key": 3}
    assert matcher != {"key": 3, "other": 4}
    assert matcher == {"key": 3, "x": 5}
    matcher = Dict({"key": 3, "other": is_string()})
    assert matcher == {"key": 3, "other": "string"}
    assert matcher == {"key": 3, "other": "string", "x": [1, 2, 3]}
    assert matcher != {"key": 3, "other": 4}
    assert matcher != {"key": 3}
    matcher = Dict({1: "one", 8.9: [1, 2, 3], "cool": is_number()})
    assert matcher == {1: "one", 8.9: [1, 2, 3], "cool": 30.5}
    assert matcher != {1: "one", 8.9: [1, 2, 3], False: "false"}
    assert matcher == {1: "one", 8.9: [1, 2, 3], False: "false", "cool": 0}
    assert matcher != {1: "one", 8.9: [1, 2, 3], "cool": "string"}
