import uuid
from datetime import datetime, time
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from pytest_matchers import (
    anything,
    assert_match,
    assert_not_match,
    between,
    case,
    contains,
    different_value,
    has_attribute,
    if_false,
    if_true,
    is_datetime,
    is_datetime_string,
    is_dict,
    is_float,
    is_instance,
    is_int,
    is_iso_8601_date,
    is_iso_8601_datetime,
    is_iso_8601_time,
    is_json,
    is_list,
    is_number,
    is_strict_dict,
    is_string,
    is_uuid,
    not_empty_string,
    one_of,
    same_value,
)
from src.tests.conftest import CustomEqual


def test_assert_match():
    assert is_instance(CustomEqual) == CustomEqual(3)
    with pytest.raises(
        AssertionError,
        match="WARNING! Comparison failed because the left object redefines the equality operator.",
    ):
        assert CustomEqual(3) == is_instance(CustomEqual)
    assert_match(is_instance(CustomEqual), CustomEqual(3))
    assert_match(CustomEqual(3), is_instance(CustomEqual))
    with pytest.raises(AssertionError):
        assert_match(is_instance(str), CustomEqual(3))


def test_assert_not_match():
    assert is_instance(str) != CustomEqual(3)
    with pytest.raises(
        AssertionError,
        match="WARNING! Comparison failed because the left object redefines the equality operator.",
    ):
        assert CustomEqual(3) != is_instance(str)
    assert_not_match(is_instance(str), CustomEqual(3))
    assert_not_match(CustomEqual(3), is_instance(str))
    with pytest.raises(AssertionError):
        assert_not_match(is_instance(CustomEqual), CustomEqual(3))


def test_anything():
    assert 3 == anything()
    assert "string" == anything()


def test_is_instance():
    assert "string" == is_instance(str)
    assert 3 != is_instance(str)


def test_is_list():
    assert [1, 2, 3] == is_list(int, length=3)
    assert [1, 2, 3] != is_list(str, length=3)
    assert [1, 2, 3] != is_list(int, length=2)
    assert [1, 2, 3] == is_list(int, min_length=2)
    assert [1, 2, 3] != is_list(int, min_length=4)
    assert [1, 2, 3] == is_list(int, max_length=4)
    assert [1, 2, 3] != is_list(int, max_length=2)
    assert ["abc"] == is_list()


def test_is_string():
    assert "string" == is_string()
    assert "" == is_string()
    assert "string" == is_string(starts_with="s")
    assert "string" == is_string(ends_with="g")
    assert "string" == is_string(contains="ri")
    assert "string" == is_string(length=6)
    assert "string" == is_string(min_length=6)
    assert "string" == is_string(max_length=6)
    assert 3 != is_string()
    assert "string" != is_string(starts_with="a")
    assert "string" != is_string(ends_with="a")
    assert "string" != is_string(contains="a")
    assert "string" != is_string(length=5)
    assert "string" != is_string(min_length=7)
    assert "string" != is_string(max_length=5)


def test_not_empty_string():
    assert "string" == not_empty_string()
    assert "" != not_empty_string()
    assert "string" != not_empty_string(min_length=7)
    assert "string" != not_empty_string(max_length=5)
    assert "string" != not_empty_string(min_length=7, max_length=5)


def test_is_number():
    assert 3 == is_number()
    assert "3" == is_number()
    assert 3 == is_number(int)
    assert 3 == is_number(min_value=2)
    assert 3 == is_number(max_value=4)
    assert 3 == is_number(min_value=2, max_value=4)
    assert "text" != is_number()
    assert "3.5" != is_number(int)
    assert 3 != is_number(float)
    assert 3 != is_number(min_value=4)
    assert 3 != is_number(max_value=2)
    assert 3 != is_number(min_value=4, max_value=2)
    assert 3 != is_number(min_value=4, max_value=7)


def test_is_int():
    assert 3 == is_int()
    assert 3.5 != is_int()
    assert 3 == is_int(min_value=2)
    assert 3 == is_int(max_value=4)
    assert 3 == is_int(min_value=2, max_value=4)
    assert 3 != is_int(min_value=4)
    assert 3 != is_int(max_value=2)
    assert 3 != is_int(min_value=4, max_value=2)
    assert 3 != is_int(min_value=4, max_value=7)


def test_is_float():
    assert 3.5 == is_float()
    assert 3 != is_float()
    assert 3.0 == is_float()
    assert 3.5 == is_float(min_value=2)
    assert 3.5 == is_float(max_value=4)
    assert 3.5 == is_float(min_value=2, max_value=4)
    assert 3.5 != is_float(min_value=4)
    assert 3.5 != is_float(max_value=2)
    assert 3.5 != is_float(min_value=4, max_value=2)
    assert 3.5 != is_float(min_value=4, max_value=7)


def test_one_of():
    assert 1 == one_of(1, 4)
    assert 4 == one_of(1, 4)
    assert 1 != one_of(2, 3)
    assert 4 == one_of(is_instance(str), is_instance(int))


def test_has_attribute():
    mock = MagicMock(attribute=30)
    assert "string" == has_attribute("lower")
    assert "string" != has_attribute("lower", "string")
    assert "string" != has_attribute("attribute")
    assert mock == has_attribute("attribute")
    assert mock == has_attribute("attribute", 30)
    assert mock != has_attribute("attribute", 40)


def test_between():
    assert 2 == between(1, 3)
    assert 1 == between(1, 3)
    assert 2 == between(1, 3, inclusive=False)
    assert 3 != between(1, 3, inclusive=False)
    assert 1 == between(1, 3, max_inclusive=False)
    assert 3 != between(1, 3, max_inclusive=False)
    assert 1 != between(1, 3, min_inclusive=False)
    assert 3 == between(1, 3, min_inclusive=False)
    assert "c" == between("a", "d")


def test_contains():
    assert ["a", "b", "c"] == contains("a")
    assert ["a", "b", "c"] == contains("a", "b")
    assert ["a", "b", "c"] == contains("a", "b", "c")
    assert ["a", "b", "c"] != contains("d")
    assert ["a", "b", "c"] != contains(["a", "b"])
    assert "Hello!" == contains("Hello")
    assert "Hello!" != contains("Hi")


def test_is_datetime():
    assert datetime(2021, 1, 1) == is_datetime()
    assert datetime(2021, 1, 1) == is_datetime(year=2021, month=1, day=1)
    assert datetime(2021, 1, 1) != is_datetime(year=2021, month=1, day=2)
    assert datetime(2021, 1, 2) == is_datetime(min_value=datetime(2021, 1, 1))
    assert datetime(2021, 1, 1) == is_datetime(max_value=datetime(2021, 1, 2))
    assert datetime(2021, 1, 1, 20, 15, 15) == is_datetime(
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2021, 1, 2),
    )
    assert datetime(2021, 1, 1, 20, 14, 15) == is_datetime(
        year=2021,
        month=1,
        day=1,
        hour=20,
        minute=14,
        second=15,
    )


def test_is_datetime_string():
    assert "2021-01-01" != is_datetime_string("erroneous_format")
    assert "2021-01-01" == is_datetime_string("%Y-%m-%d")
    assert "2021-01-01" == is_datetime_string("%Y-%m-%d")
    assert "2021-01-01" != is_datetime_string("%Y-%m-%d %H:%M:%S")
    assert "2021-01-01" == is_datetime_string("%Y-%m-%d", min_value=datetime(2021, 1, 1))
    assert "2021-01-01" == is_datetime_string("%Y-%m-%d", max_value=datetime(2021, 1, 1))
    assert "2021-01-01" == is_datetime_string(
        "%Y-%m-%d",
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2021, 1, 2),
    )
    assert "2021-01-01" != is_datetime_string(
        "%Y-%m-%d",
        min_value=datetime(2021, 1, 2),
        max_value=datetime(2021, 1, 2),
    )


def test_is_iso_8601_datetime():
    assert "2021-01-01T00:00:00" == is_iso_8601_datetime()
    assert "2021-01-01T21:00:00" == is_iso_8601_datetime(min_value=datetime(2021, 1, 1))
    assert "2021-01-01T20:00:00" == is_iso_8601_datetime(max_value=datetime(2021, 1, 2))
    assert "2021-01-01T15:00:00" == is_iso_8601_datetime(
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2021, 1, 2),
    )


def test_is_iso_8601_date():
    assert "2021-01-01" == is_iso_8601_date()
    assert "2021-01-01" == is_iso_8601_date(min_value=datetime(2021, 1, 1))
    assert "2021-01-01" == is_iso_8601_date(max_value=datetime(2021, 1, 1))
    assert "2021-01-01" == is_iso_8601_date(
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2021, 1, 2),
    )


def test_is_iso_8601_time():
    assert "00:00:00" == is_iso_8601_time()
    assert "21:00:00" == is_iso_8601_time(min_value=time(20))
    assert "20:00:00" == is_iso_8601_time(max_value=time(21))
    assert "15:00:00" == is_iso_8601_time(min_value=time(14), max_value=time(16))


def test_same_value():
    assert 3 == same_value()
    assert 4 == same_value()
    matcher = same_value()
    assert matcher == 3
    assert matcher != 4
    assert matcher == 3


def test_different_value():
    assert 3 == different_value()
    assert 4 == different_value()
    matcher = different_value()
    assert matcher == 3
    assert matcher != 3
    assert matcher == 4


def test_if_true():
    assert 3 == if_true(True, is_number(), is_string())
    assert 4 != if_true(False, is_number(), is_string())
    assert 3 == if_true(lambda x: x == 3, 3)
    assert 4 != if_true(lambda x: x == 3, 4, 3)
    assert 4 == if_true(lambda x: x == 3, 4)
    assert 3 != if_true(3, 4)
    assert 4 != if_true(3, 4, 5)
    assert 20 == if_true(is_number(int), is_number(min_value=10), is_number(max_value=10))


def test_if_false():
    assert 3 == if_false(False, is_number(), is_string())
    assert 4 != if_false(True, is_number(), is_string())
    assert 3 == if_false(lambda x: x == 3, 3)
    assert 4 == if_false(lambda x: x == 3, 4, 3)
    assert 4 == if_false(lambda x: x == 3, 4)
    assert 3 == if_false(3, 4)
    assert 4 == if_false(3, 4, 5)
    assert 20 != if_false(is_number(int), is_number(min_value=10), is_number(max_value=10))


def test_case():
    assert 4 == case(3, {3: 4, 4: "string"})
    assert "3" == case(3, {3: is_string()})
    assert 4 != case(3, {3: is_string()}, 4)
    assert "string" == case(4, {3: is_number()}, is_string())
    assert 4 != case(4, {3: 3})


def test_is_dict():
    assert {"key": 3} == is_dict()
    assert {"key": 3} == is_dict({"key": 3})
    assert {"key": 3} != is_dict({"key": 4})
    assert {"key": 3} != is_dict({"other": 3})
    assert {"key": 3} == is_dict({"key": 3}, exclude=["other"])
    assert {"key": 3, "other": 10} != is_dict({"key": 3}, exclude=["other"])
    assert {"key": 3} != is_dict({"key": 3, "other": 4})
    assert {"key": 3, "x": 5} == is_dict({"key": 3})
    assert {"key": 3, "other": "string"} == is_dict({"key": 3, "other": is_string()})
    assert {1: "one", 8.9: [1, 2, 3], "cool": 30.5} == is_dict(
        {1: "one", 8.9: [1, 2, 3], "cool": is_number()}
    )


def test_is_strict_dict():
    assert {"key": 3} != is_strict_dict({})
    assert {"key": 3} == is_strict_dict({"key": 3})
    assert {"key": 3} != is_strict_dict({"key": 4})
    assert {"key": 3, "other": 5} != is_strict_dict({"key": 3})
    assert {"key": 3, "other": 4} == is_strict_dict(
        {"key": 3},
        extra_condition=True,
        when_true={"other": 4},
        when_false={"other": 5},
    )
    assert {"key": 3, "other": 4} != is_strict_dict(
        {"key": 3},
        extra_condition=False,
        when_true={"other": 4},
        when_false={"other": 5},
    )
    assert {"key": "hey"} != is_strict_dict(
        {},
        extra_condition=False,
        when_true={"key": is_string()},
    )
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert {} == is_strict_dict({}, extra_condition=False, when_true={"key": is_string()})


def test_is_json():
    assert "{}" == is_json()
    assert '{"key": "value"}' == is_json()
    assert '{"key": 4}' == is_json({"key": 4})
    assert '{"key": 4}' != is_json({"key": 5})
    assert '{"key": 4, "other": 10}' == is_json({"key": 4})
    assert '{"key": 4}' != is_json({"other": 4})
    assert '{"key": 4}' == is_json({"key": 4}, exclude=["other"])
    assert '{"key": 4, "other": 10}' != is_json({"key": 4}, exclude=["other"])
    assert '{"key": 4, "other": "string"}' == is_json({"key": 4, "other": is_string()})


def test_is_uuid():
    assert uuid4() == is_uuid()
    assert uuid4() == is_uuid(version=4)
    assert uuid4() != is_uuid(version=5)
    assert uuid4() != is_uuid(str)
    assert str(uuid4()) == is_uuid()
    assert str(uuid4()) == is_uuid(str)
    assert str(uuid4()) != is_uuid(uuid.UUID)
