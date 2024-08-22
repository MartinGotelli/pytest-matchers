from unittest.mock import MagicMock

from pytest_matchers import is_number
from pytest_matchers.asserts.comparers.list import ListComparer


def test_compare():
    comparer = ListComparer([1, 2, 3], [1, 2, 3])
    assert comparer.compare()
    comparer = ListComparer([1, 2, 3], [1, 2, 4])
    assert not comparer.compare()
    comparer = ListComparer([1, 2, 3], [1, 2])
    assert not comparer.compare()
    comparer = ListComparer([1, 2], [1, is_number()])
    assert comparer.compare()
    comparer = ListComparer([1, 2], [2, 1])
    assert not comparer.compare()


def test_compare_fail_fast():
    mock = MagicMock()
    comparer = ListComparer([1, 2, 2, mock], [1, 2, 3, 4])
    assert not comparer.compare()
    mock.__eq__.assert_not_called()  # pylint: disable=no-member
    comparer = ListComparer([1, 2, 3, mock], [1, 2, 3, 4])
    assert not comparer.compare()
    mock.__eq__.assert_called_once_with(4)  # pylint: disable=no-member


def test_compare_fail_fast_false():
    mock = MagicMock()
    comparer = ListComparer([1, 2, 2, mock], [1, 2, 3, 4], fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_called_once_with(4)  # pylint: disable=no-member
    mock = MagicMock()
    comparer = ListComparer([1, 2, 3, mock], [1, 2, 3, 4], fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_called_once_with(4)  # pylint: disable=no-member


def test_compare_fail_fast_false_different_length():
    mock = MagicMock()
    comparer = ListComparer([1, 2, mock], [1, 2], fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_not_called()  # pylint: disable=no-member
    comparer = ListComparer([1, 2], [1, 2, mock], fail_fast=False)
    assert not comparer.compare()
    mock.__eq__.assert_not_called()  # pylint: disable=no-member
