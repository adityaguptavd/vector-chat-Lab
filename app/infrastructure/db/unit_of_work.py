from sqlalchemy.orm import Session
from app.domain.unit_of_work import AbstractUnitOfWork
from app.infrastructure.db.repositories.user_repository import UserRepository
from app.infrastructure.db.repositories.document_repository import DocumentRepository
from types import TracebackType
from typing import Optional, Type


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.user_repo = UserRepository(self.session)
        self.document_repo = DocumentRepository(self.session)
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()