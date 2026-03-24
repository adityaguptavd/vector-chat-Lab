from abc import ABC, abstractmethod
from app.domain.vector.vector_store import AbstractVectorStore


class AbstractUserVectorStoreManager(ABC):

    @abstractmethod
    def get_store(self, user_id: str) -> AbstractVectorStore:
        pass