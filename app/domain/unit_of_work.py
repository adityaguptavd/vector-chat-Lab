from abc import ABC, abstractmethod
from app.domain.repositories.user_repository import AbstractUserRepository
from types import TracebackType
from typing import Optional, Type

class AbstractUnitOfWork(ABC):

    user_repo: AbstractUserRepository

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