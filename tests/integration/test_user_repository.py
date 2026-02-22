import pytest
from app.repositories.user_repository import UserRepository
from app.domain.user import User
from app.domain.exceptions import UserAlreadyExists

# Test - 1: User creation
def test_create_user(db_session):
    repo = UserRepository(db_session)

    user = User.create(
        email="test@example.com",
        password_hash="hashed_pw"
    )

    saved_user = repo.create(user)

    assert saved_user.id is not None
    assert saved_user.email == "test@example.com"

# Test - 2: Fetch user by did
def test_get_user_by_id(db_session):
    repo = UserRepository(db_session)

    user = User.create(
        email="test@example.com",
        password_hash="hashed_password"
    )

    created = repo.create(user)

    fetched = repo.get_by_id(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.email == created.email

# Test - 3: Email uniqueness
def test_cannot_create_user_with_duplicate_email(db_session):
    repo = UserRepository(db_session)

    user1 = User.create(
        email="duplicate@example.com",
        password_hash="hashed_password"
    )

    user2 = User.create(
        email="duplicate@example.com",
        password_hash="another_hash"
    )

    repo.create(user1)

    with pytest.raises(UserAlreadyExists):
        repo.create(user2)

# Test - 4: Get user by email
def test_get_user_by_email(db_session):
    repo = UserRepository(db_session)
    user = User.create(
        email="lookup@example.com",
        password_hash="hashed_pw"
    )
    repo.create(user)

    fetched_existing = repo.get_by_email("lookup@example.com")
    fetched_not_existing = repo.get_by_email("no@example.com")

    # test existing user
    assert fetched_existing is not None
    assert fetched_existing.email == "lookup@example.com"
    assert fetched_existing.id == user.id

    # test not existing user
    assert fetched_not_existing is None

# Test - 5: Check email existence
def test_exists_by_email(db_session):
    repo = UserRepository(db_session)

    user = User.create(
        email="exists@example.com",
        password_hash="hashed_pw"
    )
    repo.create(user)

    assert repo.exists_by_email("exists@example.com") is True
    assert repo.exists_by_email("missing@example.com") is False