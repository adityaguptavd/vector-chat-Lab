from abc import ABC, abstractmethod


class AbstractPasswordHasher(ABC):

    @abstractmethod
    def hash(self, raw_password: str) -> str:
        pass

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        pass