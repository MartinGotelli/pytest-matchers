from typing import Optional

import pytest

pydantic = pytest.importorskip("pydantic")

# pylint: disable=too-few-public-methods
BaseModel = pydantic.BaseModel
Field = pydantic.Field
BaseModelV1 = pydantic.v1.BaseModel


class PersonV2(BaseModel):
    name: str
    age: int
    friends: list[str] = []


class MoneyPersonV2(PersonV2):
    money: Optional[int]
    debts: Optional[int] = Field(default_factory=int)


class PersonV1(BaseModelV1):
    name: str
    age: int
    friends: list[str] = []


@pytest.fixture
def palermo():
    return PersonV2(name="Palermo", age=30)


@pytest.fixture
def monica():
    return PersonV2(name="Mónica", age=25, friends=["Rachel", "Phoebe"])


@pytest.fixture
def roman():
    return PersonV1(name="Román", age=40)
