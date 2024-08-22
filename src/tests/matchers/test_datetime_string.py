from datetime import datetime

import pytest

from pytest_matchers.matchers import DatetimeString


def test_create():
    matcher = DatetimeString("format")
    assert isinstance(matcher, DatetimeString)
    matcher = DatetimeString("format", min_value=datetime(2021, 1, 1))
    assert isinstance(matcher, DatetimeString)
    matcher = DatetimeString("%Y-%m-%d", min_value="2020-01-01")
    assert isinstance(matcher, DatetimeString)
    matcher = DatetimeString("format", max_value=datetime(2021, 1, 1))
    assert isinstance(matcher, DatetimeString)
    with pytest.raises(
        ValueError,
        match="Invalid datetime string format for max_value: 2020-01-01",
    ):
        DatetimeString("format", max_value="2020-01-01", min_value=datetime(2021, 1, 1))


def test_repr():
    matcher = DatetimeString("format")
    assert repr(matcher) == "To be a datetime string with format 'format'"
    matcher = DatetimeString("%Y-%m-%d", min_value=datetime(2021, 1, 1, 10))
    assert (
        repr(matcher) == "To be a datetime string with format '%Y-%m-%d' "
        "greater or equal than 2021-01-01 00:00:00"
    )
    matcher = DatetimeString("%Y-%m-%d %H:%M:%S", max_value=datetime(2021, 1, 1, 10))
    assert (
        repr(matcher) == "To be a datetime string with format '%Y-%m-%d %H:%M:%S' "
        "lower or equal than 2021-01-01 10:00:00"
    )
    matcher = DatetimeString(
        "%Y-%m-%d",
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2021, 1, 2),
    )
    assert (
        repr(matcher) == "To be a datetime string with format '%Y-%m-%d' "
        "between 2021-01-01 00:00:00 and 2021-01-02 00:00:00"
    )


def test_matches():
    matcher = DatetimeString("format")
    assert matcher != "2021-01-01"
    assert matcher != 3
    assert matcher != datetime(2021, 1, 1)
    matcher = DatetimeString("%Y-%m-%d")
    assert matcher == "2021-01-01"
    assert matcher != "2020-01-01 10:20:15"
    assert matcher != "2020/06/21"
    assert matcher != "10-11-2005"
    assert matcher != datetime(2020, 1, 1)
    matcher = DatetimeString("%Y-%m-%d", min_value=datetime(2021, 1, 1))
    assert matcher == "2021-01-02"
    assert matcher == "2021-01-01"
    assert matcher != "2020-01-01"
    assert matcher != datetime(2020, 1, 1)
    matcher = DatetimeString("%Y-%m-%d", min_value=datetime(2021, 1, 1, 23, 59, 59))
    assert matcher == "2021-01-02"
    assert matcher == "2021-01-01"
    assert matcher != "2020-12-31"
    matcher = DatetimeString("%Y-%m-%d", min_value="2020-01-01")
    assert matcher == "2021-01-01"
    assert matcher != "2019-01-01"
    assert matcher != datetime(2019, 1, 1)
    matcher = DatetimeString("%Y-%m-%d", max_value=datetime(2021, 1, 1))
    assert matcher == "2021-01-01"
    assert matcher != "2022-01-01"
    assert matcher != datetime(2022, 1, 1)
    matcher = DatetimeString(
        "%Y-%m-%d",
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2021, 1, 2),
    )
    assert matcher == "2021-01-01"
    assert matcher == "2021-01-02"
    assert matcher != "2021-01-03"
    assert matcher != datetime(2021, 1, 3)
