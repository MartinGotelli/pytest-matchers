# Pytest Matchers
Test your code with vague constrains

[![Release Notes](https://img.shields.io/github/v/release/MartinGotelli/pytest-matchers.svg?style=flat-square)](https://github.com/MartinGotelli/pytest-matchers/releases)
[![CI](https://github.com/MartinGotelli/pytest-matchers/actions/workflows/python-package.yml/badge.svg)](https://github.com/MartinGotelli/pytest-matchers/actions/workflows/python-package.yml)
[![PyPI - License](https://img.shields.io/pypi/l/pytest-matchers?style=flat-square)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pytest-matchers?style=flat-square)](https://pypistats.org/packages/pytest-matchers)
[![GitHub star chart](https://img.shields.io/github/stars/MartinGotelli/pytest-matchers?style=flat-square)](https://star-history.com/#MartinGotelli/pytest-matchers)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Quick Install
With pip
```bash
pip install pytest-matchers
```

With poetry
```bash
poetry add pytest-matchers [--group dev]
```

## Usage
Examples on [tests/examples](https://github.com/MartinGotelli/pytest-matchers/tree/main/src/pytest_matchers/tests/examples)
```python
from random import random
from pytest_matchers import is_number


def test_random_number():
    assert random() == is_number(min_value=0, max_value=1)
```

And when failing:
```python
def test_random_number():
    assert random() == is_number(min_value=1, max_value=2)
```

On pytest CLI
```
=================================== FAILURES ===================================
______________________________ test_random_number ______________________________

    def test_random_number():
>       assert random() == is_number(min_value=1, max_value=2)
E       assert 0.9048172867693559 == To be a number between 1 and 2
E        +  where 0.9048172867693559 = random()
E        +  and   To be a number between 1 and 2 = is_number(min_value=1, max_value=2)

tests/examples/test_example.py:6: AssertionError
=========================== short test summary info ============================
FAILED tests/examples/test_example.py::test_random_number - assert 0.9048172867693559 == To be a number between 1 and 2
============================== 1 failed in 0.02s ===============================
```
On PyCharm
```
tests/examples/test_example.py:4 (test_random_number)
0.9048172867693559 != To be a number between 1 and 2

Expected :To be a number between 1 and 2
Actual   :0.9048172867693559
```

## Matchers
- `is_number`
- `is_string`
- `is_list`
- `is_instance`
- `between`
- `one_of`
- `has_attribute`
- `is_datetime`
- `is_datetime_string`
- `same_value`
- `different_value`
- `if_true`
- `if_false`
- `case`