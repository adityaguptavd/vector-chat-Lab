from app.domain.chat_message import ChatMessage, MessageRole
from app.domain.chat_session import ChatSession
from app.domain.user import User

from app.infrastructure.db.repositories.chat_message_repository import (
    ChatMessageRepository,
)
from app.infrastructure.db.repositories.chat_session_repository import (
    ChatSessionRepository,
)
from app.infrastructure.db.repositories.user_repository import UserRepository


def _create_session(db_session):
    user_repo = UserRepository(db_session)
    session_repo = ChatSessionRepository(db_session)

    user = user_repo.create(
        User.create(email="test@test.com", password_hash="hashed")
    )

    return session_repo.create(ChatSession.create(user_id=user.id))


def test_create_message(db_session):
    session = _create_session(db_session)

    repo = ChatMessageRepository(db_session)

    msg = ChatMessage.create(
        session_id=session.id,
        role=MessageRole.USER,
        content="hello",
    )

    created = repo.create(msg)

    assert created.id == msg.id
    assert created.session_id == session.id
    assert created.content == "hello"


def test_get_by_session_orders_chronologically(db_session):
    session = _create_session(db_session)

    repo = ChatMessageRepository(db_session)

    m1 = repo.create(
        ChatMessage.create(
            session_id=session.id,
            role=MessageRole.USER,
            content="a",
        )
    )

    m2 = repo.create(
        ChatMessage.create(
            session_id=session.id,
            role=MessageRole.USER,
            content="b",
        )
    )

    messages = repo.get_by_session(session.id)

    assert messages[0].id == m1.id
    assert messages[1].id == m2.id


def test_soft_delete(db_session):
    session = _create_session(db_session)

    repo = ChatMessageRepository(db_session)

    msg = repo.create(
        ChatMessage.create(
            session_id=session.id,
            role=MessageRole.USER,
            content="x",
        )
    )

    repo.soft_delete(msg.id)

    messages = repo.get_by_session(session.id)

    assert len(messages) == 0