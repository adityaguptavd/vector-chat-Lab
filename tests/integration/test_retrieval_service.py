from app.application.services.retrieval_service import RetrievalService
from app.schemas.vector import VectorDocument
from tests.fakes.fake_user_vector_store_manager import (
    FakeUserVectorStoreManager,
)
from tests.fakes.fake_embedder import FakeEmbedder


def test_retrieval_with_embeddings():
    manager = FakeUserVectorStoreManager()
    embedder = FakeEmbedder()

    store = manager.get_store("user1")

    chunks = ["hello world"]
    embeddings = embedder.embed(chunks)

    documents = [
        VectorDocument(
            document_id="doc1",
            chunk_id="doc1_chunk_0",
            content=chunks[0],
            embedding=embeddings[0],
            metadata={},
        )
    ]

    store.add_documents(documents)

    service = RetrievalService(manager, embedder)

    results = service.search("user1", "hello world")

    assert len(results) == 1
    assert results[0].document_id == "doc1"
    assert results[0].content == "hello world"