import pytest
from app.application.services.document_service import DocumentService
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.domain.user import User
from app.infrastructure.db.repositories.user_repository import UserRepository
from tests.fakes.fake_content_hasher import FakeContentHasher
from tests.fakes.fake_user_vector_store_manager import (
    FakeUserVectorStoreManager,
)
from app.application.services.document_ingestor import SimpleDocumentIngestor
from tests.fakes.fake_embedder import FakeEmbedder
from app.application.services.retrieval_service import RetrievalService

from app.infrastructure.vector.faiss_vector_store import FAISSVectorStore
from app.schemas.vector import VectorDocument
from app.application.services.chunker import SimpleChunker


def test_vector_store_isolation_between_users(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)

    vector_manager = FakeUserVectorStoreManager()
    embedder = FakeEmbedder()
    ingestor = SimpleDocumentIngestor(vector_manager, embedder, SimpleChunker())
    hasher = FakeContentHasher()

    service = DocumentService(
        uow=uow,
        ingestor=ingestor,
        content_hasher=hasher,
    )

    user_repo = UserRepository(db_session)

    user1 = user_repo.create(User.create("u1@test.com", "hashed"))
    user2 = user_repo.create(User.create("u2@test.com", "hashed"))

    doc1 = service.upload_document(
        user_id=user1.id,
        filename="a.txt",
        content=b"user1 content",
    )

    doc2 = service.upload_document(
        user_id=user2.id,
        filename="b.txt",
        content=b"user2 content",
    )

    retrieval = RetrievalService(vector_manager, embedder)

    results_user1 = retrieval.search(user1.id, "user1 content")
    results_user2 = retrieval.search(user2.id, "user2 content")

    # Ensure isolation via public API
    assert results_user1[0].document_id == doc1.id
    assert results_user2[0].document_id == doc2.id

    # Cross-check
    assert results_user1[0].document_id != doc2.id
    assert results_user2[0].document_id != doc1.id

def test_faiss_persistence(tmp_path):
    store = FAISSVectorStore(tmp_path, embedding_dim=3)

    doc = VectorDocument(
        document_id="doc1",
        chunk_id="chunk1",
        content="hello world",
        embedding=[0.1, 0.2, 0.3],
        metadata={},
    )

    store.add_documents([doc])

    # Simulate restart
    store = FAISSVectorStore(tmp_path, embedding_dim=3)

    results = store.similarity_search([0.1, 0.2, 0.3], top_k=1)

    assert len(results) == 1
    assert results[0].content == "hello world"