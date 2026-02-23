from app.services.retrieval_service import RetrievalService
from tests.fakes.fake_user_vector_store_manager import (
    FakeUserVectorStoreManager,
)
from tests.fakes.fake_vector_store import FakeVectorStore
from tests.fakes.fake_embedder import FakeEmbedder

def test_retrieval_with_embeddings():
    manager = FakeUserVectorStoreManager()
    embedder = FakeEmbedder()

    store = manager.get_store("user1")
    embeddings = embedder.embed(["hello world"])
    store.add_embeddings("doc1", embeddings)

    service = RetrievalService(manager, embedder)

    results = service.search("user1", "hello world")

    assert results[0][0] == "doc1"