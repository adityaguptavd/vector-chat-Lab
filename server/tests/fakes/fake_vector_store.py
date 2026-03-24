from typing import List
from app.domain.vector.vector_store import AbstractVectorStore
from app.infrastructure.vector.schemas.vector_document import VectorDocument


class FakeVectorStore(AbstractVectorStore):

    def __init__(self) -> None:
        self.documents: List[VectorDocument] = []

    def add_documents(
        self,
        documents: List[VectorDocument],
    ) -> None:
        self.documents.extend(documents)

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
    ) -> List[VectorDocument]:
        return self.documents[:top_k]