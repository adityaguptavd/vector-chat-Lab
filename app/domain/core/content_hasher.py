from abc import ABC, abstractmethod


class AbstractContentHasher(ABC):

    @abstractmethod
    def hash(self, content: bytes) -> str:
        pass