import pytest
from app.repositories.document_repository import DocumentRepository
from app.repositories.user_repository import UserRepository
from app.domain.document import Document
from app.domain.user import User

# Test - 1: Document creation
def test_create_document(db_session):
    user_repo = db_session  # we will use UserModel directly via repo
    user = User.create(
        email="doc_user@example.com",
        password_hash="hashed_pw"
    )

    saved_user = UserRepository(db_session).create(user)

    repo = DocumentRepository(db_session)

    document = Document.create(
        user_id=saved_user.id,
        filename="file.txt",
        content_hash="hash123"
    )

    saved_doc = repo.create(document)

    assert saved_doc.id is not None
    assert saved_doc.filename == "file.txt"
    assert saved_doc.user_id == saved_user.id


# Test - 2: Get document by id
def test_get_document_by_id(db_session):
    user = UserRepository(db_session).create(
        User.create("lookup_doc@example.com", "hashed")
    )

    repo = DocumentRepository(db_session)

    created = repo.create(
        Document.create(user.id, "file.txt", "hashabc")
    )

    fetched = repo.get_by_id(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.filename == "file.txt"


# Test - 3: Get documents by user
def test_get_documents_by_user(db_session):
    user = UserRepository(db_session).create(
        User.create("list_doc@example.com", "hashed")
    )

    repo = DocumentRepository(db_session)

    repo.create(Document.create(user.id, "a.txt", "hash1"))
    repo.create(Document.create(user.id, "b.txt", "hash2"))

    documents = repo.get_by_user(user.id)

    assert len(documents) == 2


# Test - 4: Get document by hash
def test_get_document_by_hash(db_session):
    user = UserRepository(db_session).create(
        User.create("hash_doc@example.com", "hashed")
    )

    repo = DocumentRepository(db_session)

    created = repo.create(
        Document.create(user.id, "file.txt", "uniquehash")
    )

    fetched_existing = repo.get_by_hash(user.id, "uniquehash")
    fetched_missing = repo.get_by_hash(user.id, "nohash")

    # existing
    assert fetched_existing is not None
    assert fetched_existing.id == created.id

    # missing
    assert fetched_missing is None


# Test - 5: Same hash allowed for different users
def test_same_hash_allowed_for_different_users(db_session):

    repo_user = UserRepository(db_session)

    user1 = repo_user.create(User.create("u1@example.com", "hashed"))
    user2 = repo_user.create(User.create("u2@example.com", "hashed"))

    repo = DocumentRepository(db_session)

    repo.create(Document.create(user1.id, "file.txt", "samehash"))
    repo.create(Document.create(user2.id, "file.txt", "samehash"))

    docs_user1 = repo.get_by_user(user1.id)
    docs_user2 = repo.get_by_user(user2.id)

    assert len(docs_user1) == 1
    assert len(docs_user2) == 1