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
    status: str
    age_restriction: str
    genre: str
    member_id: str


class UserWork(UserWorkIn):
    id: str
