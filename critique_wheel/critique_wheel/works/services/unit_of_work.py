# pylint: disable=attribute-defined-outside-init
from __future__ import annotations

import abc

from critique_wheel.adapters.sqlalchemy import work_repository as repository
from critique_wheel.infrastructure import database as db_config


class AbstractUnitOfWork(abc.ABC):
    works: repository.AbstractWorkRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class WorkUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=db_config.get_postgres_session_local()):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.works = repository.WorkRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
