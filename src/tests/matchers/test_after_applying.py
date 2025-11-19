from pytest_matchers.matchers import AfterApplying

from pytest_matchers import is_number


def _plus_2(value: int) -> int:
    return value + 2


def test_create():
    matcher = AfterApplying(lambda x: x + 1, 2)  # pragma: no branch
    assert isinstance(matcher, AfterApplying)
    matcher = AfterApplying(_plus_2, is_number())
    assert isinstance(matcher, AfterApplying)


def test_matches():
    matcher = AfterApplying(lambda x: x + 1, 2)
    assert matcher == 1
    assert matcher != 2
    assert matcher != "1"
    matcher = AfterApplying(_plus_2, is_number())
    assert matcher == 1
    assert matcher == 2
    assert matcher != "1"


def test_repr():
    matcher = AfterApplying(lambda x: x + 1, 2)  # pragma: no branch
    assert repr(matcher) == (
        "After applying the <lambda> function, the result is expected equal to 2"
    )
    matcher = AfterApplying(_plus_2, is_number())
    assert repr(matcher) == (
        "After applying the _plus_2 function, the result is expected to be a number"
    )
