from unittest.mock import MagicMock

from pytest_matchers import is_number
from pytest_matchers.asserts.comparers.dict import DictComparer


def test_compare():
    comparer = DictComparer({"a": 1, "b": 2}, {"a": 1, "b": 2})
    assert comparer.compare()
    comparer = DictComparer({"a": 1, "b": 2}, {"a": 1, "b": 3})
    assert not comparer.compare()
    comparer = DictComparer({"a": 1, "b": 2}, {"a": 1})
    assert not comparer.compare()
    comparer = DictComparer({"a": 1, "b": 2}, {"a": 1, "b": is_number()})
    assert comparer.compare()
    comparer = DictComparer({"a": 1, "b": 2}, {"b": 2, "a": 1})
    assert comparer.compare()


def test_compare_fail_fast():
    mock = MagicMock()
    comparer = DictComparer({"a": 1, "b": 3, "c": mock}, {"a": 1, "b": 2, "c": 3})
    assert not comparer.compare()
    mock.__eq__.assert_not_called()  # pylint: disable=no-member
    comparer = DictComparer({"a": 1, "b": 2, "c": mock}, {"a": 1, "b": 2, "c": 3})
    assert not comparer.compare()
    mock.__eq__.assert_called_once_with(3)  # pylint: disable=no-member


def test_compare_fail_fast_false():
    mock = MagicMock()
    comparer = DictComparer({"a": 1, "b": 3, "c": mock}, {"a": 1, "b": 2, "c": 3}, fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_called_once_with(3)  # pylint: disable=no-member
    mock = MagicMock()
    comparer = DictComparer({"a": 1, "b": 2, "c": mock}, {"a": 1, "b": 2, "c": 3}, fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_called_once_with(3)  # pylint: disable=no-member


def test_compare_fail_fast_false_different_length():
    mock = MagicMock()
    comparer = DictComparer({"a": 1, "b": 2, "c": mock}, {"a": 1, "b": 2}, fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_not_called()  # pylint: disable=no-member
    comparer = DictComparer({"a": 1, "b": 2}, {"a": 1, "b": 2, "c": mock}, fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_not_called()  # pylint: disable=no-member
