from src.main import is_instance, is_list


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
