from random import random
from unittest.mock import MagicMock

from pytest_matchers import is_instance, is_list, is_number
from pytest_matchers.main import between, has_attribute


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


def test_mock_log_exception():
    def _logging_function(logging):
        try:
            raise ValueError("This is a test exception")
        except ValueError as error:
            logging.exception(f"Caught exception: %s", error)

    mock_logging = MagicMock()
    _logging_function(mock_logging)
    mock_logging.exception.assert_called_with(
        "Caught exception: %s",
        is_instance(ValueError) & has_attribute("args", ("This is a test exception",)),
    )
