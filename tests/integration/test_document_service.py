import pytest
from app.services.document_service import DocumentService
from app.unit_of_work import SqlAlchemyUnitOfWork
from app.domain.user import User
from app.repositories.user_repository import UserRepository
from tests.fakes.fake_document_ingestor import FakeDocumentIngestor
from tests.fakes.fake_content_hasher import FakeContentHasher

# Test - 1: Upload new document
def test_upload_new_document(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    ingestor = FakeDocumentIngestor()
    hasher = FakeContentHasher()

    service = DocumentService(
        uow=uow,
        ingestor=ingestor,
        content_hasher=hasher,
    )

    user = UserRepository(db_session).create(
        User.create("doc_service@example.com", "hashed")
    )

    doc = service.upload_document(
        user_id=user.id,
        filename="file.txt",
        content=b"hello",
    )

    assert doc.filename == "file.txt"
    assert len(ingestor.calls) == 1
    assert hasher.calls[0] == b"hello"

# Test - 2: Upload duplicate document
def test_upload_duplicate_document_returns_existing(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    ingestor = FakeDocumentIngestor()
    hasher = FakeContentHasher()

    service = DocumentService(
        uow=uow,
        ingestor=ingestor,
        content_hasher=hasher,
    )

    user = UserRepository(db_session).create(
        User.create("dup_service@example.com", "hashed")
    )

    first = service.upload_document(
        user_id=user.id,
        filename="file.txt",
        content=b"same",
    )

    second = service.upload_document(
        user_id=user.id,
        filename="file.txt",
        content=b"same",
    )

    assert first.id == second.id
    assert len(ingestor.calls) == 1