from typing import List

from app.domain.chat_message import ChatMessage, MessageRole
from app.domain.chat_session import ChatSession
from app.domain.exceptions import NotFoundError, ForbiddenError
from app.domain.unit_of_work import AbstractUnitOfWork
from app.application.services.rag_chat_service import RAGChatService

from app.core.logging.logger import LoggingManager
from app.application.dto.chat import ChatSessionResult, ChatMessageResult

logger = LoggingManager.get_logger("chat_service")


class ChatService:

    def __init__(
        self,
        uow: AbstractUnitOfWork,
        rag_chat_service: RAGChatService,
    ) -> None:
        self.uow = uow
        self._rag = rag_chat_service

    # ---------------- SESSION ----------------

    def create_session(self, user_id: str, title: str | None = None) -> ChatSessionResult:
        with self.uow:
            session = ChatSession.create(user_id=user_id, title=title)
            created = self.uow.chat_sessions_repo.create(session)
        return ChatSessionResult.model_validate(created)

    def list_sessions(self, user_id: str) -> List[ChatSessionResult]:
        with self.uow:
            sessions = self.uow.chat_sessions_repo.get_by_user(user_id)
        return [ChatSessionResult.model_validate(session) for session in sessions]

    def archive_session(self, user_id: str, session_id: str) -> ChatSessionResult:
        with self.uow:
            session = self._get_owned_session(user_id, session_id)

            session.archive()
            updated = self.uow.chat_sessions_repo.update(session)
        return ChatSessionResult.model_validate(updated)

    # ---------------- MESSAGE ----------------

    async def add_user_message_and_generate(
        self,
        *,
        user_id: str,
        session_id: str,
        content: str,
    ) -> str:

        logger.debug(
            "Chat message attempt",
            extra={"event": "chat_attempt", "user_id": user_id, "session_id": session_id},
        )

        with self.uow:

            session: ChatSession = self._get_owned_session(
                user_id=user_id,
                session_id=session_id,
            )

            if session.is_archived:
                logger.warning(
                    "Chat blocked: archived session",
                    extra={"event": "chat_blocked_archived", "session_id": session_id},
                )
                raise ValueError("Cannot send messages to archived session")

            user_msg = ChatMessage.create(
                session_id=session.id,
                role=MessageRole.USER,
                content=content,
            )

            self.uow.chat_messages_repo.create(user_msg)

            session.touch()
            self.uow.chat_sessions_repo.update(session)

        response_text = await self._rag.chat(
            user_id=user_id,
            query=content,
        )

        with self.uow:

            ai_msg = ChatMessage.create(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=response_text,
            )

            self.uow.chat_messages_repo.create(ai_msg)

        logger.info(
            "Chat message success",
            extra={"event": "chat_success", "user_id": user_id, "session_id": session_id},
        )

        return response_text

    def send_message(
        self,
        user_id: str,
        session_id: str,
        content: str,
        role: MessageRole = MessageRole.USER,
    ) -> ChatMessageResult:

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

        return ChatMessageResult.model_validate(created)

    def list_messages(self, user_id: str, session_id: str) -> List[ChatMessageResult]:
        with self.uow:
            self._get_owned_session(user_id, session_id)
            messages = self.uow.chat_messages_repo.get_by_session(session_id)

        return [ChatMessageResult.model_validate(message) for message in messages]

    # ---------------- INTERNAL ----------------

    def _get_owned_session(self, user_id: str, session_id: str) -> ChatSession:
        session = self.uow.chat_sessions_repo.get_by_id(session_id)

        if not session:
            raise NotFoundError("Chat session not found")

        if session.user_id != user_id:
            raise ForbiddenError("Access denied")

        return session