import pytest
from pathlib import Path

from app.infrastructure.vector.local_embedder import (
    LocalSentenceTransformerEmbedder,
)
from app.infrastructure.vector.faiss_user_vector_store_manager import (
    FAISSUserVectorStoreManager,
)
from app.application.services.chunker import SimpleChunker
from app.application.services.document_ingestor import SimpleDocumentIngestor
from app.application.services.retrieval_service import RetrievalService

@pytest.mark.slow
def test_real_semantic_retrieval(tmp_path: Path):
    embedder = LocalSentenceTransformerEmbedder()

    manager = FAISSUserVectorStoreManager(
        base_path=tmp_path,
        embedding_dim=embedder.dimension,
    )

    chunker = SimpleChunker()

    ingestor = SimpleDocumentIngestor(
        user_vector_manager=manager,
        embedder=embedder,
        chunker=chunker,
    )

    retrieval = RetrievalService(manager, embedder)

    ingestor.ingest(
        user_id="user1",
        document_id="doc1",
        content="Python is a popular programming language.",
    )

    results = retrieval.search("user1", "What is Python?")

    assert len(results) > 0
    assert "Python" in results[0].content