from typing import Type

from pydantic import BaseModel
from pydantic.v1 import BaseModel as BaseModelV1

from pytest_matchers.pydantic.matchers import PydanticModel


def is_pydantic(
    model_class: Type[BaseModel | BaseModelV1] | None = None,
    *,
    strict: bool = None,
    exempt_defaults: bool = True,
    attributes: dict = None,
    **kwargs,
):
    model_class = model_class or BaseModel
    if strict is None:
        strict = bool(attributes) or bool(kwargs)
    return PydanticModel(
        model_class,
        strict=strict,
        exempt_defaults=exempt_defaults,
        attributes=attributes,
        **kwargs,
    )


def is_pydantic_v1(
    model_class: Type[BaseModelV1] | None = None,
    *,
    strict: bool = None,
    exempt_defaults: bool = True,
    attributes: dict = None,
    **kwargs,
):
    return is_pydantic(
        model_class or BaseModelV1,
        strict=strict,
        exempt_defaults=exempt_defaults,
        attributes=attributes,
        **kwargs,
    )
