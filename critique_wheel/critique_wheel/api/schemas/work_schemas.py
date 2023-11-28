from pydantic import BaseModel

from critique_wheel.critiques.value_objects import CritiqueId
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.value_objects import Content, Title, WorkId


class WorkPayloadSchema(BaseModel):
    title: Title
    content: Content
    member_id: MemberId
    genre: str
    age_restriction: str
    critiques: list[CritiqueId] = []


class WorkResponseSchema(BaseModel):
    id: WorkId
    title: Title
    content: Content
    age_restriction: str
    genre: str
    member_id: MemberId
    critiques: list[CritiqueId] = []
