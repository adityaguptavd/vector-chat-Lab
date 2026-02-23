from abc import ABC, abstractmethod
from typing import List, Tuple


class AbstractVectorStore(ABC):

    @abstractmethod
    def add_embeddings(
        self,
        document_id: str,
        embeddings: List[List[float]],
    ) -> None:
        pass

    @abstractmethod
    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
    ) -> List[Tuple[str, float]]:
        pass