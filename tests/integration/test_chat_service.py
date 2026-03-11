from app.application.services.chat_service import ChatService
from app.domain.user import User

from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.db.repositories.user_repository import UserRepository


def _create_user(db_session):
    return UserRepository(db_session).create(
        User.create(email="test@test.com", password_hash="hashed")
    )


def _service(db_session):
    return ChatService(SqlAlchemyUnitOfWork(db_session))


# ---------------- SESSION ----------------


def test_create_session(db_session):
    user = _create_user(db_session)
    service = _service(db_session)

    session = service.create_session(user.id, title="t1")

    assert session.user_id == user.id
    assert session.title == "t1"


def test_list_sessions(db_session):
    user = _create_user(db_session)
    service = _service(db_session)

    s1 = service.create_session(user.id)
    s2 = service.create_session(user.id)

    sessions = service.list_sessions(user.id)

    assert len(sessions) == 2
    assert sessions[0].id in {s1.id, s2.id}


def test_archive_session(db_session):
    user = _create_user(db_session)
    service = _service(db_session)

    session = service.create_session(user.id)
    archived = service.archive_session(user.id, session.id)

    assert archived.is_archived is True


# ---------------- MESSAGE ----------------


def test_send_message_flow(db_session):
    user = _create_user(db_session)
    service = _service(db_session)

    session = service.create_session(user.id)

    msg = service.send_message(user.id, session.id, "hello")

    assert msg.content == "hello"
    assert msg.session_id == session.id


def test_list_messages(db_session):
    user = _create_user(db_session)
    service = _service(db_session)

    session = service.create_session(user.id)

    service.send_message(user.id, session.id, "a")
    service.send_message(user.id, session.id, "b")

    messages = service.list_messages(user.id, session.id)

    assert len(messages) == 2
    assert messages[0].content == "a"
    assert messages[1].content == "b"


def test_archive_blocks_messages(db_session):
    user = _create_user(db_session)
    service = _service(db_session)

    session = service.create_session(user.id)
    service.archive_session(user.id, session.id)

    try:
        service.send_message(user.id, session.id, "x")
    except Exception:
        assert True
    else:
        assert False