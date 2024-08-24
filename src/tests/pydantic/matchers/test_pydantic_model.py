import pytest
from pydantic import BaseModel

from pytest_matchers import anything, is_list, is_number, is_string
from pytest_matchers.pydantic.matchers import PydanticModel
from src.tests.pydantic.conftest import MoneyPersonV2, PersonV1, PersonV2


def test_create():
    with pytest.raises(ValueError, match="Consider using strict=False"):
        PydanticModel(PersonV2)
    matcher = PydanticModel(PersonV2, strict=False)
    assert isinstance(matcher, PydanticModel)
    matcher = PydanticModel(PersonV2, name="Palermo", age=30)
    assert isinstance(matcher, PydanticModel)
    with pytest.raises(ValueError, match="Attributes {'age'} are not present"):
        PydanticModel(PersonV2, name="Palermo")
    matcher = PydanticModel(PersonV2, name="Palermo", strict=False)
    assert isinstance(matcher, PydanticModel)
    with pytest.raises(ValueError, match="Attributes {'friends'} are not present"):
        PydanticModel(PersonV2, name="Palermo", age=30, exempt_defaults=False)
    matcher = PydanticModel(
        PersonV2,
        name="Palermo",
        age=30,
        exempt_defaults=False,
        strict=False,
    )
    assert isinstance(matcher, PydanticModel)


def test_repr():
    matcher = PydanticModel(PersonV2, strict=False)
    assert repr(matcher) == "To be a pydantic model instance of 'PersonV2'"
    matcher = PydanticModel(PersonV2, name="Palermo", age=30, strict=False)
    assert (
        repr(matcher) == "To be a pydantic model instance of 'PersonV2' "
        "with 'name' being 'Palermo' and with 'age' being 30"
    )
    matcher = PydanticModel(PersonV2, name="Palermo", age=30)
    assert (
        repr(matcher) == "To be a pydantic model instance of 'PersonV2' "
        "with 'name' being 'Palermo' and with 'age' being 30 and "
        "with 'friends' being []"
    )
    matcher = PydanticModel(PersonV2, name="Palermo", age=30, friends=is_list())
    assert repr(matcher) == (
        "To be a pydantic model instance of 'PersonV2' "
        "with 'name' being 'Palermo' and with 'age' being 30 and "
        "with 'friends' expected of 'list' instance"
    )
    matcher = PydanticModel(PersonV1, name=is_string(), age=is_number())
    assert repr(matcher) == (
        "To be a pydantic model instance of 'PersonV1' "
        "with 'name' expected to be a string and with 'age' expected to be a number and "
        "with 'friends' being []"
    )


def test_base_model_repr():
    matcher = PydanticModel(BaseModel, strict=False)
    assert repr(matcher) == "To be a pydantic model instance of 'BaseModel'"
    matcher = PydanticModel(BaseModel, name="Palermo")
    assert (
        repr(matcher) == "To be a pydantic model instance of 'BaseModel' "
        "with 'name' being 'Palermo'"
    )


def test_matches_strict(palermo, monica, roman):
    matcher = PydanticModel(PersonV2, name="Palermo", age=30)
    assert matcher == palermo
    assert matcher != monica
    assert matcher != roman
    assert matcher != "Palermo"
    matcher = PydanticModel(PersonV2, name=roman.name, age=roman.age)
    assert matcher != palermo
    assert matcher != monica
    assert matcher != roman  # Román is a TestModelV1 instance
    matcher = PydanticModel(PersonV2, name=is_string(), age=is_number(max_value=28))
    assert matcher != palermo
    assert matcher != monica  # Mónica has friends
    assert matcher != roman
    matcher = PydanticModel(PersonV2, name=is_string(), age=is_number(), friends=is_list())
    assert matcher == palermo
    assert matcher == monica
    assert matcher != roman
    matcher = PydanticModel(PersonV1, name=is_string(), age=is_number(), friends=is_list())
    assert matcher != palermo
    assert matcher != monica
    assert matcher == roman


def test_matches_non_strict(palermo, monica, roman):
    matcher = PydanticModel(PersonV2, strict=False)
    assert matcher == palermo
    assert matcher == monica
    assert matcher != roman
    matcher = PydanticModel(PersonV2, name="Palermo", strict=False)
    assert matcher == palermo
    assert matcher != monica
    assert matcher != roman
    matcher = PydanticModel(PersonV2, friends=["Rachel", "Phoebe"], strict=False)
    assert matcher != palermo
    assert matcher == monica
    assert matcher != roman


def test_matches_exempt_default(palermo, monica, roman):
    matcher = PydanticModel(
        PersonV2,
        name=is_string(),
        age=is_number(),
        friends=["Rachel", "Phoebe"],
        exempt_defaults=False,
    )
    assert matcher != palermo
    assert matcher == monica
    assert matcher != roman
    matcher = PydanticModel(
        PersonV2,
        name="Palermo",
        age=30,
        friends=is_list(),
        exempt_defaults=False,
    )
    assert matcher == palermo
    assert matcher != monica
    assert matcher != roman
    matcher = PydanticModel(
        PersonV2,
        name=is_string(),
        age=is_number(),
        exempt_defaults=False,
        strict=False,
    )
    assert matcher == palermo
    assert matcher == monica
    assert matcher != roman


def test_matches_sub_model():
    seba = MoneyPersonV2(name="Sebastián", age=35, money=1000)
    diego = MoneyPersonV2(name="Diego", age=30, money=None, debts=500)
    matcher = PydanticModel(MoneyPersonV2, name=seba.name, age=seba.age, money=seba.money)
    assert matcher == seba
    assert matcher != diego
    matcher = PydanticModel(MoneyPersonV2, name=seba.name, age=seba.age, strict=False)
    assert matcher == seba
    assert matcher != diego
    matcher = PydanticModel(MoneyPersonV2, name=is_string(), age=is_number(), money=anything())
    assert matcher == seba
    assert matcher != diego
    matcher = PydanticModel(MoneyPersonV2, name=is_string(), age=is_number(), strict=False)
    assert matcher == seba
    assert matcher == diego


def test_reserved_attributes():
    class StrictModel(BaseModel):
        name: str
        strict: str
        attributes: list = []

    model = StrictModel(name="Strict!", strict="No")
    matcher = PydanticModel(StrictModel, name=model.name, attributes={"strict": model.strict})
    assert matcher == model
    matcher = PydanticModel(
        StrictModel,
        name=model.name,
        attributes={"strict": model.strict, "attributes": model.attributes},
        exempt_defaults=False,
    )
    assert matcher == model
    matcher = PydanticModel(
        StrictModel,
        attributes={"strict": model.strict, "name": "Wrong"},
        name=model.name,
    )
    assert matcher != model


def test_matches_base_model(palermo, monica):
    matcher = PydanticModel(BaseModel, name="Palermo", age=30)
    assert matcher == palermo
    assert matcher != monica
    matcher = PydanticModel(BaseModel, strict=False)
    assert matcher == palermo
    assert matcher == monica
    matcher = PydanticModel(BaseModel, name=is_string(), age=is_number())
    assert matcher == palermo
    assert matcher != monica
