from pytest_matchers import is_string
from pytest_matchers.matchers import ExceptionMatcher


def test_create():
    matcher = ExceptionMatcher()
    assert isinstance(matcher, ExceptionMatcher)
    matcher = ExceptionMatcher(Exception)
    assert isinstance(matcher, ExceptionMatcher)
    matcher = ExceptionMatcher(Exception, "message")
    assert isinstance(matcher, ExceptionMatcher)
    matcher = ExceptionMatcher(Exception, "message", True)
    assert isinstance(matcher, ExceptionMatcher)


def test_matches_type():
    matcher = ExceptionMatcher()
    assert matcher == Exception()
    assert matcher != ValueError()
    assert matcher != "string"
    matcher = ExceptionMatcher(ValueError)
    assert matcher != Exception()
    assert matcher == ValueError()
    matcher = ExceptionMatcher(Exception, match_subclass=True)
    assert matcher == Exception()
    assert matcher == ValueError()


def test_matches_message():
    matcher = ExceptionMatcher(message="message")
    assert matcher == Exception("message")
    assert matcher != Exception("another message")
    assert matcher != Exception()
    assert matcher != ValueError("message")
    matcher = ExceptionMatcher(Exception, "message")
    assert matcher == Exception("message")
    assert matcher != Exception("another message")
    assert matcher != Exception()
    assert matcher != ValueError("message")
    matcher = ExceptionMatcher(Exception, "message", True)
    assert matcher == Exception("message")
    assert matcher != Exception("another message")
    assert matcher != Exception()
    assert matcher == ValueError("message")
    matcher = ExceptionMatcher(Exception, "")
    assert matcher == Exception()
    assert matcher != Exception("message")
    assert matcher == Exception("")
    matcher = ExceptionMatcher(Exception, is_string(starts_with="message"))
    assert matcher == Exception("message")
    assert matcher == Exception("message and more")
    assert matcher != Exception("another message")


def test_repr():
    matcher = ExceptionMatcher()
    assert repr(matcher) == "To be an exception of type Exception"
    matcher = ExceptionMatcher(ValueError)
    assert repr(matcher) == "To be an exception of type ValueError"
    matcher = ExceptionMatcher(ValueError, "message")
    assert repr(matcher) == (
        "To be an exception of type ValueError with message expected equal to 'message'"
    )
    matcher = ExceptionMatcher(ValueError, "message", True)
    assert repr(matcher) == (
        "To be an exception instance of ValueError with message expected equal to 'message'"
    )
    matcher = ExceptionMatcher(ValueError, is_string(starts_with="message"))
    assert repr(matcher) == (
        "To be an exception of type ValueError "
        "with message expected to be a string with start expected equal to 'message'"
    )
