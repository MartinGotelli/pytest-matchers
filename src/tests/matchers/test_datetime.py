from datetime import datetime

from pytest_matchers.matchers import Datetime


def test_create():
    matcher = Datetime()
    assert isinstance(matcher, Datetime)
    matcher = Datetime(min_value=datetime(2021, 1, 1))
    assert isinstance(matcher, Datetime)
    matcher = Datetime(max_value=datetime(2021, 1, 1))
    assert isinstance(matcher, Datetime)
    matcher = Datetime(year=2021)
    assert isinstance(matcher, Datetime)
    matcher = Datetime(month=1)
    assert isinstance(matcher, Datetime)
    matcher = Datetime(day=1)
    assert isinstance(matcher, Datetime)
    matcher = Datetime(
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2022, 10, 1),
        year=2021,
        month=1,
        day=1,
        hour=10,
        minute=30,
        second=45,
    )
    assert isinstance(matcher, Datetime)


def test_repr():
    matcher = Datetime()
    assert repr(matcher) == "To be a datetime"
    matcher = Datetime(min_value=datetime(2021, 1, 1), max_value=datetime(2021, 1, 2))
    assert repr(matcher) == "To be a datetime between 2021-01-01 00:00:00 and 2021-01-02 00:00:00"
    matcher = Datetime(min_value=datetime(2021, 1, 1))
    assert repr(matcher) == "To be a datetime greater or equal than 2021-01-01 00:00:00"
    matcher = Datetime(max_value=datetime(2021, 1, 1))
    assert repr(matcher) == "To be a datetime lower or equal than 2021-01-01 00:00:00"
    matcher = Datetime(year=2021)
    assert repr(matcher) == "To be a datetime with 'year' being 2021"
    matcher = Datetime(month=1)
    assert repr(matcher) == "To be a datetime with 'month' being 1"
    matcher = Datetime(day=1)
    assert repr(matcher) == "To be a datetime with 'day' being 1"
    matcher = Datetime(
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2022, 10, 1),
        year=2021,
        month=1,
        day=1,
        hour=10,
        minute=30,
        second=45,
    )
    assert repr(matcher) == (
        "To be a datetime between 2021-01-01 00:00:00 and 2022-10-01 00:00:00 "
        "and with 'year' being 2021 "
        "and with 'month' being 1 "
        "and with 'day' being 1 "
        "and with 'hour' being 10 "
        "and with 'minute' being 30 "
        "and with 'second' being 45"
    )


def test_matches_instance():
    matcher = Datetime()
    assert matcher == datetime(2021, 1, 1)
    assert matcher == datetime(2021, 1, 1, 10, 30, 45)
    assert matcher != 2021
    assert matcher != "2021-01-01"


def test_matches_limit():
    matcher = Datetime(min_value=datetime(2021, 1, 1), max_value=datetime(2021, 1, 2))
    assert matcher == datetime(2021, 1, 1, 10, 30, 45)
    assert matcher == datetime(2021, 1, 2)
    assert matcher == datetime(2021, 1, 1)
    assert matcher != datetime(2021, 1, 2, 10, 30, 45)
    assert matcher != datetime(2021, 1, 2, 10, 30, 46)
    assert matcher != datetime(2021, 1, 3)
    matcher = Datetime(min_value=datetime(2021, 1, 1))
    assert matcher == datetime(2021, 1, 1)
    assert matcher == datetime(2021, 1, 2)
    assert matcher == datetime(2090, 1, 1)
    assert matcher != datetime(2020, 12, 31)
    matcher = Datetime(max_value=datetime(2021, 1, 1))
    assert matcher == datetime(2021, 1, 1)
    assert matcher == datetime(2020, 12, 31)
    assert matcher == datetime(1020, 1, 1)
    assert matcher != datetime(2021, 1, 2)


def test_matches_year():
    matcher = Datetime(year=2021)
    assert matcher == datetime(2021, 1, 1)
    assert matcher == datetime(2021, 12, 31)
    assert matcher != datetime(2020, 12, 31)
    assert matcher != datetime(2022, 1, 1)


def test_matches_month():
    matcher = Datetime(month=1)
    assert matcher == datetime(2021, 1, 1)
    assert matcher == datetime(2021, 1, 31)
    assert matcher != datetime(2021, 2, 1)
    assert matcher != datetime(2021, 12, 31)


def test_matches_day():
    matcher = Datetime(day=1)
    assert matcher == datetime(2021, 1, 1)
    assert matcher == datetime(2024, 10, 1, 10, 30, 45)
    assert matcher != datetime(2021, 1, 31)
    assert matcher != datetime(2021, 2, 28)


def test_matches_hour():
    matcher = Datetime(hour=10)
    assert matcher == datetime(2021, 1, 1, 10)
    assert matcher == datetime(2021, 1, 1, 10, 30)
    assert matcher != datetime(2021, 1, 1, 9)
    assert matcher != datetime(2021, 1, 1, 11)


def test_matches_minute():
    matcher = Datetime(minute=30)
    assert matcher == datetime(2021, 1, 1, 10, 30)
    assert matcher == datetime(2021, 1, 1, 10, 30, 45)
    assert matcher != datetime(2021, 1, 1, 10, 29)
    assert matcher != datetime(2021, 1, 1, 10, 31)


def test_matches_second():
    matcher = Datetime(second=45)
    assert matcher == datetime(2021, 1, 1, 10, 30, 45)
    assert matcher == datetime(2024, 10, 11, 21, 15, 45, 1000)
    assert matcher != datetime(2021, 1, 1, 10, 30, 44)
    assert matcher != datetime(2021, 1, 1, 10, 30, 46)
    assert matcher != datetime(2021, 1, 1, 10, 30)
