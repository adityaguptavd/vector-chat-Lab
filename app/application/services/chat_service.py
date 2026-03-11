from typing import List

from app.domain.chat_message import ChatMessage, MessageRole
from app.domain.chat_session import ChatSession
from app.domain.exceptions import NotFoundError, ForbiddenError
from app.domain.unit_of_work import AbstractUnitOfWork


class ChatService:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    # ---------------- SESSION ----------------

    def create_session(self, user_id: str, title: str | None = None) -> ChatSession:
        with self.uow:
            session = ChatSession.create(user_id=user_id, title=title)
            created = self.uow.chat_sessions_repo.create(session)
        return created

    def list_sessions(self, user_id: str) -> List[ChatSession]:
        with self.uow:
            return self.uow.chat_sessions_repo.get_by_user(user_id)

    def archive_session(self, user_id: str, session_id: str) -> ChatSession:
        with self.uow:
            session = self._get_owned_session(user_id, session_id)

            session.archive()
            updated = self.uow.chat_sessions_repo.update(session)
        return updated

    # ---------------- MESSAGE ----------------

    def send_message(
        self,
        user_id: str,
        session_id: str,
        content: str,
        role: MessageRole = MessageRole.USER,
    ) -> ChatMessage:

        with self.uow:
            session = self._get_owned_session(user_id, session_id)

            if session.is_archived:
                raise ForbiddenError("Cannot send message to archived session")

            msg = ChatMessage.create(
                session_id=session.id,
                role=role,
                content=content,
            )

            created = self.uow.chat_messages_repo.create(msg)

            session.touch()
            self.uow.chat_sessions_repo.update(session)

        return created

    def list_messages(self, user_id: str, session_id: str) -> List[ChatMessage]:
        with self.uow:
            self._get_owned_session(user_id, session_id)
            return self.uow.chat_messages_repo.get_by_session(session_id)

    # ---------------- INTERNAL ----------------

    def _get_owned_session(self, user_id: str, session_id: str) -> ChatSession:
        session = self.uow.chat_sessions_repo.get_by_id(session_id)

        if not session:
            raise NotFoundError("Chat session not found")

        if session.user_id != user_id:
            raise ForbiddenError("Access denied")

        return session