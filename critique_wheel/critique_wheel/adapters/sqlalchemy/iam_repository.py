from typing import Optional

from sqlalchemy.orm import Session

from critique_wheel.domain.models.IAM import Member
from critique_wheel.domain.models.iam_repository import AbstractMemberRepository


class SqlAlchemyMemberRepository(AbstractMemberRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, member: Member) -> None:
        self.session.add(member)

    def get(self, member_id: str) -> Optional[Member]:
        return self.session.query(Member).filter_by(id=member_id).one_or_none()

    def get_member_by_email(self, email: str) -> Optional[Member]:
        return self.session.query(Member).filter_by(email=email).one_or_none()

    def list(self) -> list[Member]:
        return self.session.query(Member).all()
