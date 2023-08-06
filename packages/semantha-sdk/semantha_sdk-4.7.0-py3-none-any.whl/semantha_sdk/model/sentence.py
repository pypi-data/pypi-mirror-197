from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from marshmallow_dataclass import class_schema

from semantha_sdk.model.named_entity import NamedEntity
from semantha_sdk.model.reference import Reference
from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Sentence(SemanthaModelEntity):
    id: str
    text: str
    document_name: Optional[str]
    named_entities: Optional[List[NamedEntity]]
    references: Optional[List[Reference]]


SentenceSchema = class_schema(Sentence, base_schema=SemanthaSchema)
