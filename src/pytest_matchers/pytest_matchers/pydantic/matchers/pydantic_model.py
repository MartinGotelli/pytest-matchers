from typing import Any, Type

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic.v1 import BaseModel as BaseModelV1
from pydantic.v1.fields import ModelField

from pytest_matchers.matchers import HasAttribute, Matcher
from pytest_matchers.utils.matcher_utils import is_instance_matcher
from pytest_matchers.utils.repr_utils import concat_reprs


def _model_fields(model_class: Type[BaseModel | BaseModelV1]):
    if issubclass(model_class, BaseModelV1):
        return model_class.__fields__
    return model_class.model_fields


def _is_required(field: FieldInfo | ModelField) -> bool:
    if isinstance(field, ModelField):
        return field.required
    return field.is_required()


def _default_value(field: FieldInfo | ModelField) -> Any:
    if field.default_factory is None:
        return field.default
    return field.default_factory()


def _version(model_class: Type) -> str | None:
    is_pydantic = hasattr(model_class, "__pydantic_complete__") or hasattr(
        model_class, "__fields__"
    )
    if is_pydantic:
        if hasattr(model_class, "__pydantic_complete__"):
            return "v2"
        return "v1"
    return None


class PydanticModel(Matcher):
    def __init__(
        self,
        model_class: Type[BaseModel | BaseModelV1],
        *,
        strict: bool = True,
        exempt_defaults: bool = True,
        attributes: dict = None,
        **kwargs,
    ):
        super().__init__()
        self._model_class = model_class
        self._is_instance_matcher = is_instance_matcher(model_class)
        self._strict = strict
        self._exempt_defaults = exempt_defaults
        self._attributes = kwargs
        self._attributes.update(attributes or {})
        self._assert_matching_all_attributes()

    def _assert_matching_all_attributes(self):
        if not self._strict:
            return
        fields = _model_fields(self._model_class)
        if self._exempt_defaults:
            fields = {name: field for name, field in fields.items() if _is_required(field)}
        attribute_names = set(self._attributes.keys())
        model_attribute_names = set(fields.keys())
        missing_attributes = model_attribute_names - attribute_names
        if missing_attributes:
            raise ValueError(
                f"Attributes {missing_attributes} are not present in "
                f"{self._model_class.__name__}.\n"
                "Consider using strict=False"
            )

    def _optional_matchers(self, value: Any = None) -> list[Matcher]:
        if value is None:
            model_class = self._model_class
        else:
            model_class = type(value)
        if self._strict and self._exempt_defaults:
            fields = _model_fields(model_class)
            return [
                HasAttribute(name, _default_value(field))
                for name, field in fields.items()
                if not _is_required(field) and name not in self._attributes
            ]
        return []

    def _attribute_matchers(self, value: Any = None) -> list[Matcher]:
        return [
            HasAttribute(name, value) for name, value in self._attributes.items()
        ] + self._optional_matchers(value)

    def matches(self, value: Any) -> bool:
        return self._matches_instance(value) and all(
            matcher == value for matcher in self._attribute_matchers(value)
        )

    def _matches_instance(self, value: Any) -> bool:
        expected_model_version = _version(self._model_class)
        value_version = _version(type(value))
        return expected_model_version == value_version and self._is_instance_matcher == value

    def __repr__(self) -> str:
        return concat_reprs(
            f"To be a pydantic model instance of {repr(self._model_class.__name__)}",
            *self._attribute_matchers(),
        )
