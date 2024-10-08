import uuid
from datetime import datetime
from random import random
from unittest.mock import MagicMock
from uuid import NAMESPACE_DNS, uuid3, uuid4, uuid5

from pytest_matchers import (
    anything,
    assert_match,
    between,
    case,
    different_value,
    has_attribute,
    if_false,
    if_true,
    is_datetime,
    is_datetime_string,
    is_dict,
    is_instance,
    is_list,
    is_number,
    is_pydantic,
    is_strict_dict,
    is_string,
    is_uuid,
    one_of,
    same_value,
)
from src.tests.conftest import CustomEqual
from src.tests.pydantic.conftest import BaseModel


def test_deal_with_custom_equals():
    assert not CustomEqual(3) == is_instance(CustomEqual)  # pylint: disable=unnecessary-negation
    assert is_instance(CustomEqual) == CustomEqual(3)
    assert_match(CustomEqual(3), is_instance(CustomEqual))


def test_random_number():
    assert random() == is_number(min_value=0, max_value=1)
    assert random() == between(0, 1)


def test_dict_comparison():
    value = {
        "string": "string",
        "int": 3,
        "list": [1, 2, 3],
    }
    assert value == {
        "string": is_instance(str),
        "int": is_instance(int),
        "list": is_list(int, length=3),
    }
    assert value != {"string": is_instance(str), "int": is_instance(int)}


def test_mock_log_exception():
    def _logging_function(logging):
        try:
            raise ValueError("This is a test exception")
        except ValueError as error:
            logging.exception("Caught exception: %s", error)

    mock_logging = MagicMock()
    _logging_function(mock_logging)
    mock_logging.exception.assert_called_with(
        "Caught exception: %s",
        is_instance(ValueError) & has_attribute("args", ("This is a test exception",)),
    )


def test_datetime_comparison():
    def _datetime_function():
        return {
            "data": "some data",
            "created_at": datetime.now(),
            "created_at_string": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    expected_value = {
        "data": "some data",
        "created_at": is_datetime(min_value=datetime.now()),
        "created_at_string": is_datetime_string("%Y-%m-%d %H:%M:%S", min_value=datetime.now()),
    }
    first_data = _datetime_function()
    assert first_data == expected_value
    second_data = _datetime_function()
    assert second_data == expected_value
    assert first_data != second_data


def test_same_and_different_value_comparison():
    dynamic_value = None

    def _function(previous_value: float = 0):
        nonlocal dynamic_value
        if dynamic_value is None:
            dynamic_value = random()
        return {
            "static": "static",
            "dynamic_repeated": dynamic_value,
            "dynamic_different": previous_value + random(),
        }

    expected_value = {
        "static": "static",
        "dynamic_repeated": same_value() & is_number(min_value=0, max_value=1),
        "dynamic_different": different_value() & is_number(),
    }
    first_data = _function()
    assert first_data == expected_value
    second_data = _function(first_data["dynamic_different"])
    assert second_data == expected_value


def test_conditional_matchers():
    assert random() == if_true(
        lambda value: value > 0.5,
        is_number(min_value=0.5, inclusive=False),
        is_number(max_value=0.5),
    )
    assert random() == if_false(
        lambda value: value > 0.5,
        is_number(max_value=0.5),
        is_number(min_value=0.5, inclusive=False),
    )
    random_value = random()
    random_string = "low"
    if random_value > 0.5:  # pragma: no cover
        random_string = "medium"
    if random_value > 0.8:  # pragma: no cover
        random_string = "high"
    assert random_value == case(
        random_string,
        {
            "low": is_number(max_value=0.5),
            "medium": is_number(min_value=0.5, max_value=0.8, min_inclusive=False),
            "high": is_number(min_value=0.8, inclusive=False),
        },
    )
    matcher = if_true(is_string(), is_datetime_string("%Y-%m-%d"), is_datetime())
    assert "2021-01-01" == matcher
    assert datetime(2021, 1, 1) == matcher
    assert 3 != matcher
    assert random() != matcher
    assert "10/11/2029" != matcher


def test_compare_dictionaries():
    test_dict = {"a": 1, "b": [2, "string"], "c": True, "d": "true"}

    assert test_dict == {
        "a": 1,
        "b": is_list(length=2),
        "c": True,
        "d": anything(),
    }
    assert test_dict != {
        "a": 1,
        "b": is_list(length=2),
        "c": True,
    }
    assert test_dict == is_dict(
        {
            "a": 1,
            "b": is_list(length=2),
            "c": True,
        }
    )
    assert test_dict != is_dict(
        {
            "a": 1,
            "b": is_list(length=2),
            "c": True,
        },
        exclude=["d"],
    )
    assert test_dict == is_dict(
        {
            "a": 1,
            "b": is_list(length=2),
            "c": True,
        },
        exclude=["e"],
    )


def test_compare_strict_dictionaries():
    def _condition(value):
        return value == is_string()

    test_dict = {"a": 1, "b": [2, "string"], "c": True}
    assert test_dict == is_strict_dict({"a": 1, "b": [2, "string"], "c": True})
    assert test_dict != is_strict_dict({"a": 1, "b": [2, "string"]})
    assert test_dict == is_strict_dict(
        {"a": 1, "b": [2, "string"]},
        extra_condition=_condition("string"),
        when_true={"c": True},
        when_false={"c": False},
    )
    assert test_dict != is_strict_dict(
        {"a": 1, "b": [2, "string"]},
        extra_condition=_condition(10),
        when_true={"c": True},
        when_false={"c": False},
    )


def test_is_string_with_created_datetime_matcher():
    now = datetime.now()
    date_format = "%Y-%m-%d %H:%M:%S"
    now_string = now.strftime(date_format)
    assert now_string == is_datetime_string(date_format)
    start_text = f"{now_string}: Martín created this awesome test"
    assert start_text == is_string(starts_with=is_datetime_string(date_format))
    end_text = f"Someone decided to add some extra text to the end on: {now_string}"
    assert end_text == is_string(ends_with=is_datetime_string(date_format))
    contains_text = f"I once ate a sandwich, was on {now_string}, or maybe two"
    assert contains_text == is_string(contains=is_datetime_string(date_format))
    assert start_text == is_string(contains=is_datetime_string(date_format))
    assert end_text == is_string(contains=is_datetime_string(date_format))


def test_uuids():
    assert uuid4() == is_uuid()
    assert str(uuid4()) == is_uuid()
    assert uuid4() != is_uuid(version=1)
    assert uuid4() == is_uuid(version=4)
    assert str(uuid4()) != is_uuid(uuid.UUID)
    assert uuid4() != is_uuid(str)
    for uuid_value in (uuid3(NAMESPACE_DNS, "python.org"), uuid4()):
        assert uuid_value == is_uuid(version=one_of(3, 4))
    assert uuid5(NAMESPACE_DNS, "python.org") != is_uuid(version=one_of(3, 4))


def test_pydantic():
    class Animal(BaseModel):  # pylint: disable=too-few-public-methods
        age: int
        name: str

    class Human(Animal):  # pylint: disable=too-few-public-methods
        money: float = 0

    class Dog(Animal):  # pylint: disable=too-few-public-methods
        breed: str = "Mongrel"

    messi = Human(age=33, name="Messi")
    lassie = Dog(age=3, name="Lassie", breed="Collie")
    tweety = Animal(age=1, name="Tweety")

    assert_match(messi, is_pydantic())
    assert_match(lassie, is_pydantic())
    assert_match(messi, is_pydantic(Human))
    assert_match(lassie, is_pydantic(Dog, age=3, name="Lassie", breed="Collie"))
    assert_match(tweety, is_pydantic(age=1))
    assert_match(messi, is_pydantic(Human, age=33, strict=False))
