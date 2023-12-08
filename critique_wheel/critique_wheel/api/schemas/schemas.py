from pydantic import BaseModel


class UserCritiquesIn(BaseModel):
    member_id: str
    content: str
    work_id: str


class UserCritiques(UserCritiquesIn):
    id: str


class UserWorkIn(BaseModel):
    title: str
    content: str
    member_id: str
    genre: str
    age_restriction: str
    critiques: list[UserCritiques] = []


class UserWork(UserWorkIn):
    id: str
