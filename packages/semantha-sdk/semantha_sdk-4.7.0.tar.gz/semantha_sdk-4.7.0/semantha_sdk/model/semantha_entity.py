from abc import ABC
from dataclasses import dataclass
from typing import Type

from marshmallow import Schema
import humps


@dataclass(frozen=True)
class SemanthaModelEntity(ABC):
    pass


def with_entity(cls: Type[SemanthaModelEntity]):
    class WithEntity:
        _entity_class = cls

    return WithEntity


class SemanthaSchema(Schema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = humps.camelize(field_obj.data_key or field_name)
