from app.domain.services.document_ingestor import AbstractDocumentIngestor
from app.domain.vector.user_vector_store_manager import (
    AbstractUserVectorStoreManager,
)
from app.domain.vector.embedder import AbstractEmbedder
from app.domain.services.chunker import AbstractChunker
from app.schemas.vector import VectorDocument


class SimpleDocumentIngestor(AbstractDocumentIngestor):

    def __init__(
        self,
        user_vector_manager: AbstractUserVectorStoreManager,
        embedder: AbstractEmbedder,
        chunker: AbstractChunker
    ) -> None:
        self.user_vector_manager = user_vector_manager
        self.embedder = embedder
        self.chunker = chunker

    def ingest(
        self,
        user_id: str,
        document_id: str,
        content: str,
    ) -> None:

        store = self.user_vector_manager.get_store(user_id)

        chunks = self.chunker.chunk(content)

        embeddings = self.embedder.embed(chunks)

        documents = []

        for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            documents.append(
                VectorDocument(
                    document_id=document_id,
                    chunk_id=f"{document_id}_chunk_{idx}",
                    content=chunk_text,
                    embedding=embedding,
                    metadata={},
                )
            )

        store.add_documents(documents)