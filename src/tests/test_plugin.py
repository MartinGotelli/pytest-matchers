import pytest

from pytest_matchers import is_instance, is_string
from src.tests.conftest import CustomEqual


def _low_pytest_version():
    return int(pytest.__version__[0]) < 8


@pytest.fixture(autouse=True)
def _set_verbosity(request):
    previous_verbosity = request.config.option.verbose
    request.config.option.verbose = 2
    yield
    request.config.option.verbose = previous_verbosity


def _expected_base(actual, expected, operator):
    return f"assert {actual!r} {operator} {expected!r}"


def _expected_warning(actual, expected, operator):
    return _expected_base(actual, expected, operator) + (
        "\n  \n"
        "  WARNING! Comparison failed because the left object redefines the equality operator.\n"
        "  Consider using the 'assert_match' or 'assert_not_match' functions instead.\n"
        "  assert_match(actual, expected)"
    )


def _expected_list_diff(results: list) -> str:
    message = ["", "", "Full diff:", "  ["]
    batch_adds = []
    for value in results:
        if isinstance(value, tuple):
            actual, expected = value
            message.append(f"-     {repr(expected)},")
            batch_adds.append(f"+     {repr(actual)},")
        else:
            message.extend(batch_adds)
            batch_adds = []
            message.append(f"      {repr(value)},")
    message.extend(batch_adds)
    message.append("  ]")
    return "\n  ".join(message)


@pytest.mark.skipif(
    _low_pytest_version(),
    reason="The custom assert_repr is only available in pytest 8 or higher.",
)
def test_non_custom_assert_repr():
    actual = "string"
    expected = is_instance(int)
    try:
        assert actual == expected
    except AssertionError as error:
        assert str(error) == _expected_base(actual, expected, "==")


def test_custom_assert_repr():
    actual = CustomEqual(3)
    expected = is_instance(CustomEqual)
    try:
        assert actual == expected
    except AssertionError as error:
        assert str(error) == _expected_warning(actual, expected, "==")


def test_custom_assert_repr_not():
    actual = CustomEqual(3)
    expected = is_instance(str)
    try:
        assert actual != expected
    except AssertionError as error:
        assert str(error) == _expected_warning(actual, expected, "!=")


def test_custom_assert_repr_dictionary():
    custom = CustomEqual(3)
    actual = {
        "string": "string",
        "custom": custom,
        "list": [1, 2, 3],
    }
    expected = {
        "string": is_instance(str),
        "custom": is_instance(CustomEqual),
        "list": is_instance(list),
    }
    try:
        assert actual == expected
    except AssertionError as error:
        assert str(error) == _expected_warning(actual, expected, "==")


@pytest.mark.skipif(
    _low_pytest_version(),
    reason="The custom assert_repr is only available in pytest 8 or higher.",
)
def test_custom_assert_repr_dictionary_matcher_replace():
    custom = CustomEqual(3)
    actual = {
        "string": "string",
        "custom": custom,
        "list": [1, 2, 3],
    }
    expected = {
        "string": is_instance(str),
        "custom": is_instance(str),
        "list": is_instance(list),
    }
    expected_diff = (
        "\n  \n"
        "  Common items:\n"
        "  {'list': [1, 2, 3], 'string': 'string'}\n"
        "  \n"
        "  Full diff:\n"
        "    {\n"
        "  -     'custom': To be instance of 'str',\n"
        "  -     'list': [1, 2, 3],\n"
        f"  +     'custom': {custom},\n"
        "  +     'list': [\n"
        "  +         1,\n"
        "  +         2,\n"
        "  +         3,\n"
        "  +     ],\n"
        "        'string': 'string',\n"
        "    }"
    )
    try:
        assert actual == expected
    except AssertionError as error:
        assert str(error) == _expected_base(actual, expected, "==") + expected_diff


def test_custom_assert_repr_list():
    custom = CustomEqual(3)
    actual = [custom, "hey"]
    expected = [is_instance(CustomEqual), is_string()]
    try:
        assert actual == expected
    except AssertionError as error:
        assert str(error) == _expected_warning(actual, expected, "==")


@pytest.mark.skipif(
    _low_pytest_version(),
    reason="The custom assert_repr is only available in pytest 8 or higher.",
)
def test_custom_assert_repr_list_matcher_replace():
    custom = CustomEqual(3)
    actual = ["hey", custom]
    expected = [is_string(), is_instance(str)]
    try:
        assert actual == expected
    except AssertionError as error:
        assert str(error) == _expected_base(actual, expected, "==") + _expected_list_diff(
            ["hey", (custom, is_instance(str))]
        )


def test_not_equal_operator():
    actual = "string"
    expected = is_instance(str)
    try:
        assert actual != expected
    except AssertionError as error:
        assert str(error) == _expected_base(actual, expected, "!=")
