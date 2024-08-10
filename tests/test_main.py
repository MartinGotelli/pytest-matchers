from src.main import is_instance, is_list, is_number, is_string, one_of


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


def test_is_instance_matcher():
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
