from typing import List, Tuple
from app.domain.vector.vector_store import AbstractVectorStore


class FakeVectorStore(AbstractVectorStore):

    def __init__(self) -> None:
        self.vectors = {}  # document_id -> embedding

    def add_embeddings(
        self,
        document_id: str,
        embeddings: List[List[float]],
    ) -> None:
        # For prototype assume one embedding per document
        self.vectors[document_id] = embeddings[0]

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
    ) -> List[Tuple[str, float]]:
        results = []

        for doc_id, embedding in self.vectors.items():
            # naive similarity: inverse absolute distance
            score = 1 / (1 + abs(embedding[0] - query_embedding[0]))
            results.append((doc_id, score))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]