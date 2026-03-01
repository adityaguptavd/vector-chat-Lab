from abc import ABC, abstractmethod
from typing import List

from app.schemas.vector import VectorDocument


class AbstractVectorStore(ABC):

    @abstractmethod
    def add_documents(
        self,
        documents: List[VectorDocument],
    ) -> None:
        pass

    @abstractmethod
    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
    ) -> List[VectorDocument]:
        pass