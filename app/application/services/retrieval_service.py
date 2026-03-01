from app.domain.vector.user_vector_store_manager import (
    AbstractUserVectorStoreManager,
)
from app.domain.vector.embedder import AbstractEmbedder
from app.domain.vector.vector_store import AbstractVectorStore
from typing import List
from app.schemas.vector import VectorDocument


class RetrievalService:

    def __init__(
        self,
        user_vector_manager: AbstractUserVectorStoreManager,
        embedder: AbstractEmbedder,
    ) -> None:
        self.user_vector_manager = user_vector_manager
        self.embedder = embedder

    def search(
        self,
        user_id: str,
        query: str,
        top_k: int = 5,
    ) -> List[VectorDocument]:
        store: AbstractVectorStore = self.user_vector_manager.get_store(user_id)

        query_embedding = self.embedder.embed([query])[0]

        return store.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
        )