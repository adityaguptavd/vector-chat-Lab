import pytest
from app.services.document_service import DocumentService
from app.unit_of_work import SqlAlchemyUnitOfWork
from app.domain.user import User
from app.repositories.user_repository import UserRepository
from tests.fakes.fake_content_hasher import FakeContentHasher
from tests.fakes.fake_user_vector_store_manager import (
    FakeUserVectorStoreManager,
)
from app.services.document_ingestor import SimpleDocumentIngestor
from tests.fakes.fake_embedder import FakeEmbedder
from app.services.retrieval_service import RetrievalService


def test_vector_store_isolation_between_users(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)

    vector_manager = FakeUserVectorStoreManager()
    embedder = FakeEmbedder()
    ingestor = SimpleDocumentIngestor(vector_manager, embedder)
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
    assert results_user1[0][0] == doc1.id
    assert results_user2[0][0] == doc2.id

    # Cross-check
    assert results_user1[0][0] != doc2.id
    assert results_user2[0][0] != doc1.id