from sqlalchemy.orm import Session
from typing import Optional
from critique_wheel.domain.models.IAM import Member
from critique_wheel.domain.models.iam_repository import AbstractMemberRepository
from tests.unit.test_IAM import member

class SqlAlchemyMemberRepository(AbstractMemberRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, member: Member) -> None:
        self.session.add(member)

    def get(self, member_id: str) -> Optional[Member]:
        return self.session.query(Member).filter_by(id=member_id).one_or_none()

    def list(self) -> list[Member]:
        return self.session.query(Member).all()
