from abc import ABC, abstractmethod
from typing import Optional
from app.domain.user import User


class AbstractUserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass