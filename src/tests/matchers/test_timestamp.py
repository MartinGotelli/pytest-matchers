from datetime import datetime, timedelta

from pytest_matchers.matchers import Timestamp


def test_create():
    matcher = Timestamp()
    assert isinstance(matcher, Timestamp)
    matcher = Timestamp(min_value=0, max_value=1)
    assert isinstance(matcher, Timestamp)
    matcher = Timestamp(min_value=0)
    assert isinstance(matcher, Timestamp)


def test_repr():
    matcher = Timestamp()
    assert repr(matcher) == "To be a timestamp"
    matcher = Timestamp(min_value=0)
    assert repr(matcher) == "To be a timestamp greater or equal than 0"
    matcher = Timestamp(max_value=1)
    assert repr(matcher) == "To be a timestamp lower or equal than 1"
    matcher = Timestamp(min_value=0, max_value=1)
    assert repr(matcher) == "To be a timestamp between 0 and 1"


def test_matches():
    matcher = Timestamp()
    assert matcher == 0.0
    assert matcher == 1.0
    assert matcher != "string"
    assert matcher == 20
    assert matcher != ["string"]
    assert matcher != datetime.now()
    assert matcher == datetime.now().timestamp()


def test_matches_with_limit():
    now_timestamp = datetime.now().timestamp()
    tomorrow_timestamp = datetime.now().timestamp() + 86400
    matcher = Timestamp(min_value=now_timestamp, max_value=tomorrow_timestamp)
    assert matcher == now_timestamp
    assert matcher == now_timestamp + 2000
    assert matcher == tomorrow_timestamp
    assert matcher == int(now_timestamp + 2000)
    assert matcher != now_timestamp - 86400
    assert matcher != tomorrow_timestamp + 86400


def test_matches_with_datetime_limit():
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    matcher = Timestamp(min_value=now, max_value=tomorrow)
    assert matcher == now.timestamp()
    assert matcher == now.timestamp() + 2000
    assert matcher == tomorrow.timestamp()
    assert matcher == int(now.timestamp() + 2000)
    assert matcher != now.timestamp() - 86400
    assert matcher != tomorrow.timestamp() + 86400
