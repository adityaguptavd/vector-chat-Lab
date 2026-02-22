import pytest
from app.services.user_service import UserService
from app.unit_of_work import SqlAlchemyUnitOfWork
from app.domain.exceptions import UserAlreadyExists, InvalidCredentials, InvalidToken
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.fake_token_provider import FakeTokenProvider

# Test - 1: Register user
def test_register_user_success(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    service = UserService(uow=uow, password_hasher=FakePasswordHasher(), token_provider=FakeTokenProvider())

    user = service.register_user(
        email="service@example.com",
        raw_password="pw"
    )

    assert user.email == "service@example.com"

# Test - 2: Regsiter user with duplicate email
def test_register_user_duplicate(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    service = UserService(uow=uow, password_hasher=FakePasswordHasher(), token_provider=FakeTokenProvider())

    service.register_user(
        email="duplicate_service@example.com",
        raw_password="pw"
    )

    with pytest.raises(UserAlreadyExists):
        service.register_user(
            email="duplicate_service@example.com",
            raw_password="another_pw"
        )

# Test - 3: Login user
def test_login_success(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    service = UserService(
        uow=uow,
        password_hasher=FakePasswordHasher(),
        token_provider=FakeTokenProvider(),
    )

    service.register_user(
        email="test@example.com",
        raw_password="password123",
    )

    result = service.login_user(
        email="test@example.com",
        raw_password="password123",
    )

    assert result.user_id is not None
    assert result.access_token.startswith("fake-token-for-")

# Test - 4: Invalid Email Login
def test_login_invalid_email(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    service = UserService(uow=uow, password_hasher=FakePasswordHasher(), token_provider=FakeTokenProvider())
    with pytest.raises(InvalidCredentials):
        service.login_user(
            email="wrong@example.com",
            raw_password="password123",
        )

# Test - 5: Invalid Password Login
def test_login_invalid_password(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    service = UserService(uow=uow, password_hasher=FakePasswordHasher(), token_provider=FakeTokenProvider())
    service.register_user(
        email="test@example.com",
        raw_password="password123",
    )

    with pytest.raises(InvalidCredentials):
        service.login_user(
            email="test@example.com",
            raw_password="wrongpass",
        )

# Test - 6: Get user from token
def test_get_user_from_token_success(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    service = UserService(
        uow=uow,
        password_hasher=FakePasswordHasher(),
        token_provider=FakeTokenProvider(),
    )

    user = service.register_user(
        email="token@example.com",
        raw_password="pw",
    )

    login_result = service.login_user(
        email="token@example.com",
        raw_password="pw",
    )

    resolved_user = service.get_user_from_token(
        login_result.access_token
    )

    assert resolved_user.id == user.id

# Test - 7: Invalid Token Case
def test_get_user_from_invalid_token(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    service = UserService(
        uow=uow,
        password_hasher=FakePasswordHasher(),
        token_provider=FakeTokenProvider(),
    )

    with pytest.raises(InvalidToken):
        service.get_user_from_token("bad-token")