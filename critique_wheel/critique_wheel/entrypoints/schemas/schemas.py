from pydantic import BaseModel, ConfigDict


class UserCritiquesIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_id: str
    content: str
    work_id: str


class UserCritiques(UserCritiquesIn):
    id: str


class UserWorkIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    status: str
    age_restriction: str
    genre: str
    member_id: str


class UserWork(UserWorkIn):
    id: str


class UserMemberIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str
    email: str


class UserMember(UserMemberIn):
    id: str


class UserMemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
