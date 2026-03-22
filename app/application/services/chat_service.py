from typing import List, AsyncGenerator, Tuple

from app.domain.chat_message import ChatMessage, MessageRole
from app.domain.chat_session import ChatSession
from app.domain.exceptions import NotFoundError, ForbiddenError
from app.domain.unit_of_work import AbstractUnitOfWork
from app.application.services.rag_chat_service import RAGChatService
from app.core.utils.llm_validator import LLMResponseValidator
from app.core.responses import StreamResponseBuilder

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
    ) -> List[ChatMessageResult]:

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

        return [ChatMessageResult.model_validate(user_msg), ChatMessageResult.model_validate(ai_msg)]

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

    def store_user_message(self, user_id: str, session_id: str, content: str) -> Tuple[ChatSession, ChatMessage]:
        with self.uow:
            session = self._get_owned_session(user_id, session_id)

            if session.is_archived:
                raise ForbiddenError("Cannot send messages to archived session")
            # -------- STORE USER -------- #

            user_msg = ChatMessage.create(
                session_id=session.id,
                role=MessageRole.USER,
                content=content,
            )

            self.uow.chat_messages_repo.create(user_msg)
            session.touch()
            self.uow.chat_sessions_repo.update(session)

        return session, user_msg

    async def stream_message(
        self,
        session: ChatSession,
        user_msg: ChatMessage,
        content: str,
        user_id: str
    ) -> AsyncGenerator[str, None]:
        try:

            logger.debug(
                "Streaming chat attempt",
                extra={"event": "chat_stream_attempt", "user_id": user_id, "session_id": session.id},
            )

            # -------- STREAM -------- #
            full_response = ""

            try:
                async for chunk in self._rag.stream_chat(
                    user_id=user_id,
                    query=content
                ):
                    full_response += chunk
                    yield StreamResponseBuilder.chunk(chunk)

            except Exception as e:
                logger.error("LLM_GENERATION_FAILED", extra={"event": "llm_generation_failure", "user_id": user_id, "session_id": session.id, "error": str(e)})
                yield StreamResponseBuilder.error("Streaming failed")
                return

            # -------- VALIDATION -------- #
            validation_failed = False

            try:
                validated = LLMResponseValidator.validate(full_response)
            except Exception as e:
                validation_failed = True
                logger.error("LLM_VALIDATION_FAILED", extra={"event": "llm_validation_failure", "user_id": user_id, "session_id": session.id, "error": str(e)})

            # -------- STORE AI -------- #
            ai_msg = None

            if not validation_failed:
                try:
                    with self.uow:
                        ai_msg = ChatMessage.create(
                            session_id=session.id,
                            role=MessageRole.ASSISTANT,
                            content=validated,
                        )
                        self.uow.chat_messages_repo.create(ai_msg)
                        session.touch()
                        self.uow.chat_sessions_repo.update(session)

                except Exception as e:
                    logger.error(
                        "AI_MESSAGE_PERSIST_FAILED",
                        extra={
                            "event": "ai_persist_failure",
                            "user_id": user_id,
                            "session_id": session.id,
                            "error": str(e),
                        },
                    )
                    ai_msg = None

            # -------- POST STREAM SIGNALS -------- #

            if validation_failed:
                yield StreamResponseBuilder.warning(
                    "Response may be unreliable"
                )

            payload = {
                "user_message": ChatMessageResult.model_validate(user_msg).model_dump(mode="json")
                if user_msg else None,

                "ai_message": ChatMessageResult.model_validate(ai_msg).model_dump(mode="json")
                if ai_msg else None
            }

            yield StreamResponseBuilder.end(payload)

            logger.info(
                    "Streaming chat success",
                    extra={"event": "chat_stream_success", "user_id": user_id, "session_id": session.id},
                )
        except Exception as e:
            logger.error(
                "Unexpected error occured while streaming",
                extra={"event": "chat_stream_failed", "user_id": user_id, "session_id": session.id, "error": str(e)}
            )
            yield StreamResponseBuilder.error("Unexpected error occured")