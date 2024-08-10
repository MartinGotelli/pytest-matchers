from unittest.mock import MagicMock

from pytest_matchers.main import (
    between,
    has_attribute,
    is_instance,
    is_list,
    is_number,
    is_string,
    one_of,
)


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
