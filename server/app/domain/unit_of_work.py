from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type

from app.domain.repositories.user_repository import AbstractUserRepository
from app.domain.repositories.document_repository import AbstractDocumentRepository
from app.domain.repositories.chat_message_repository import AbstractChatMessageRepository
from app.domain.repositories.chat_session_repository import AbstractChatSessionRepository

class AbstractUnitOfWork(ABC):

    user_repo: AbstractUserRepository
    document_repo: AbstractDocumentRepository
    chat_sessions_repo: AbstractChatSessionRepository
    chat_messages_repo: AbstractChatMessageRepository

    @abstractmethod
    def __enter__(self) -> "AbstractUnitOfWork":
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass