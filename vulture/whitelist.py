from pytest_matchers.plugin import pytest_assertrepr_compare
from src.tests.conftest import pytest_configure
from src.tests.examples.test_example import test_pydantic
from src.tests.pydantic.conftest import MoneyPersonV2
from src.tests.test_plugin import _set_verbosity

pytest_configure
pytest_assertrepr_compare
_set_verbosity

MoneyPersonV2.friends
MoneyPersonV2.debts
test_pydantic().Dog.breed
