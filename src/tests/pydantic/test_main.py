import pydantic
import pytest
from packaging import version

from pytest_matchers import anything, assert_match, is_string
from pytest_matchers.main import contains
from pytest_matchers.pydantic.main import is_pydantic, is_pydantic_v1
from pytest_matchers.pydantic.matchers import PydanticModel
from src.tests.pydantic.conftest import PersonV1, PersonV2

if version.parse(pydantic.__version__) < version.parse("2.0"):  # pragma: no cover
    pytest.skip("pydantic version is lower than 2.0", allow_module_level=True)


def test_create_is_pydantic():
    with pytest.raises(ValueError, match="Consider using strict=False"):
        is_pydantic(PersonV2, strict=True)
    matcher = is_pydantic(PersonV2)
    assert isinstance(matcher, PydanticModel)
    with pytest.raises(ValueError, match="Attributes {'age'} are not present"):
        is_pydantic(PersonV2, name="Palermo")
    matcher = is_pydantic(PersonV2, name=anything(), age=anything())
    assert isinstance(matcher, PydanticModel)
    with pytest.raises(ValueError, match="Attributes {'friends'} are not present"):
        is_pydantic(PersonV2, name="Palermo", age=30, exempt_defaults=False)


def test_is_pydantic_without_attributes(palermo, monica, roman):
    assert palermo == is_pydantic()
    assert monica == is_pydantic()
    assert roman != is_pydantic()  # Román is v1
    assert 3 != is_pydantic()


def test_is_pydantic_v1_without_attributes(palermo, monica, roman):
    assert palermo != is_pydantic_v1()
    assert monica != is_pydantic_v1()
    assert_match(roman, is_pydantic_v1())


def test_is_pydantic_with_model_class(palermo, monica, roman):
    assert palermo == is_pydantic(model_class=PersonV2)
    assert monica == is_pydantic(model_class=PersonV2)
    assert roman != is_pydantic(model_class=PersonV2)
    assert roman != is_pydantic(model_class=PersonV1)  # BaseModel v1 implements equality
    assert_match(roman, is_pydantic(model_class=PersonV1))


def test_is_pydantic_no_class_with_attributes_strict(palermo, monica, roman):
    assert palermo == is_pydantic(name=is_string(), age=30)
    assert monica == is_pydantic(name="Mónica", age=25, friends=["Rachel", "Phoebe"])
    assert roman != is_pydantic(name="Román", age=40)
    assert monica != is_pydantic(name="Mónica", age=25)


def test_is_pydantic_with_attributes_strict(palermo, monica, roman):
    assert palermo == is_pydantic(PersonV2, name="Palermo", age=30)
    assert monica == is_pydantic(PersonV2, name="Mónica", age=25, friends=["Rachel", "Phoebe"])
    assert roman != is_pydantic(PersonV2, name="Román", age=40)
    assert_match(roman, is_pydantic(PersonV1, name="Román", age=40))
    assert monica != is_pydantic(PersonV2, name="Mónica", age=25)
    assert palermo != is_pydantic(PersonV2, name="Palermo", age=30, friends=["Román"])


def test_is_pydantic_no_class_with_attributes_non_strict(palermo, monica, roman):
    assert palermo == is_pydantic(name="Palermo", strict=False)
    assert monica == is_pydantic(name="Mónica", age=25, strict=False)
    assert roman != is_pydantic(name="Román", strict=False)
    assert monica == is_pydantic(friends=contains("Phoebe"), strict=False)


def test_is_pydantic_with_attributes_non_strict(palermo, monica, roman):
    assert palermo == is_pydantic(PersonV2, name="Palermo", strict=False)
    assert monica == is_pydantic(PersonV2, name="Mónica", age=25, strict=False)
    assert roman != is_pydantic(PersonV2, age=40, strict=False)
    assert_match(roman, is_pydantic(PersonV1, age=40, strict=False))
    assert monica == is_pydantic(PersonV2, friends=contains("Phoebe"), strict=False)


def test_is_pydantic_no_class_with_not_exempt_defaults(palermo, monica, roman):
    assert palermo == is_pydantic(name=is_string(), age=30, friends=[], exempt_defaults=False)
    assert monica == is_pydantic(
        name="Mónica",
        age=25,
        friends=["Rachel", "Phoebe"],
        exempt_defaults=False,
    )
    assert roman != is_pydantic(name="Román", age=40, friends=[], exempt_defaults=False)
    assert monica != is_pydantic(name="Mónica", age=25, friends=[], exempt_defaults=False)
