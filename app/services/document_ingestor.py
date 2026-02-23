from app.domain.services.document_ingestor import AbstractDocumentIngestor
from app.domain.vector.user_vector_store_manager import (
    AbstractUserVectorStoreManager,
)
from app.domain.vector.embedder import AbstractEmbedder


class SimpleDocumentIngestor(AbstractDocumentIngestor):

    def __init__(
        self,
        user_vector_manager: AbstractUserVectorStoreManager,
        embedder: AbstractEmbedder,
    ) -> None:
        self.user_vector_manager = user_vector_manager
        self.embedder = embedder

    def ingest(
        self,
        user_id: str,
        document_id: str,
        content: str,
    ) -> None:

        store = self.user_vector_manager.get_store(user_id)

        embeddings = self.embedder.embed([content])

        store.add_embeddings(
            document_id=document_id,
            embeddings=embeddings,
        )