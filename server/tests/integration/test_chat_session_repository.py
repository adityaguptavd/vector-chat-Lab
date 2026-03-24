from app.domain.chat_session import ChatSession
from app.domain.user import User
from app.infrastructure.db.repositories.chat_session_repository import (
    ChatSessionRepository,
)
from app.infrastructure.db.repositories.user_repository import UserRepository


def _create_user(db_session):
    user_repo = UserRepository(db_session)

    user = User.create(
        email="test@test.com",
        password_hash="hashed",
    )

    return user_repo.create(user)


def test_create_chat_session(db_session):
    user = _create_user(db_session)

    repo = ChatSessionRepository(db_session)

    session = ChatSession.create(user_id=user.id, title="t1")
    created = repo.create(session)

    assert created.id == session.id
    assert created.user_id == user.id
    assert created.title == "t1"


def test_get_by_id(db_session):
    user = _create_user(db_session)

    repo = ChatSessionRepository(db_session)
    chat = repo.create(ChatSession.create(user_id=user.id))

    found = repo.get_by_id(chat.id)

    assert found is not None
    assert found.id == chat.id


def test_get_by_user_orders_latest_first(db_session):
    user = _create_user(db_session)

    repo = ChatSessionRepository(db_session)

    s1 = repo.create(ChatSession.create(user_id=user.id))
    s2 = repo.create(ChatSession.create(user_id=user.id))

    s1.touch()
    repo.update(s1)

    sessions = repo.get_by_user(user.id)

    assert sessions[0].id == s1.id
    assert sessions[1].id == s2.id


def test_update_archive(db_session):
    user = _create_user(db_session)

    repo = ChatSessionRepository(db_session)

    session = repo.create(ChatSession.create(user_id=user.id))
    session.archive()

    updated = repo.update(session)

    assert updated.is_archived is True