from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.chat_message import ChatMessage
from .base_repository import BaseRepository
from app.domain.repositories.chat_message_repository import (
    AbstractChatMessageRepository,
)
from app.infrastructure.db.models.chat_message_model import ChatMessageModel


class ChatMessageRepository(
    BaseRepository[ChatMessageModel],
    AbstractChatMessageRepository
):

    def __init__(self, db: Session):
        super().__init__(db, ChatMessageModel)

    def create(self, message: ChatMessage) -> ChatMessage:
        model = ChatMessageModel.from_domain(message)
        saved = super().create(model)
        return saved.to_domain()

    def get_by_id(
        self,
        message_id: str,
        include_deleted: bool = False
    ) -> Optional[ChatMessage]:

        model = super().get_by_id(message_id, include_deleted=include_deleted)
        return model.to_domain() if model else None

    def get_by_session(
        self,
        session_id: str,
        *,
        page: int = 1,
        limit: int = 50
    ) -> List[ChatMessage]:

        stmt = select(self.model)

        stmt = self._apply_filters(stmt, {
            "session_id": session_id
        })

        stmt = self._apply_not_deleted(stmt)
        stmt = self._apply_ordering(stmt, "created_at")
        stmt = self._paginate(stmt, page, limit)

        results = self._execute(stmt)

        return [m.to_domain() for m in results]

    def soft_delete(self, message_id: str) -> None:
        super().soft_delete(message_id)