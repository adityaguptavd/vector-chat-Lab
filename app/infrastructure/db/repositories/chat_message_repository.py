from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.domain.chat_message import ChatMessage
from app.domain.repositories.chat_message_repository import (
    AbstractChatMessageRepository,
)
from app.infrastructure.db.models.chat_message_model import ChatMessageModel


class ChatMessageRepository(AbstractChatMessageRepository):

    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, message: ChatMessage) -> ChatMessage:
        model = ChatMessageModel.from_domain(message)
        self.db.add(model)
        self.db.flush()
        return model.to_domain()

    def get_by_id(self, message_id: str) -> Optional[ChatMessage]:
        model = self.db.get(ChatMessageModel, message_id)
        return model.to_domain() if model else None

    def get_by_session(self, session_id: str) -> List[ChatMessage]:
        stmt = (
            select(ChatMessageModel)
            .where(
                ChatMessageModel.session_id == session_id,
                ChatMessageModel.is_deleted.is_(False),
            )
            .order_by(ChatMessageModel.created_at.asc())
        )

        results = self.db.execute(stmt).scalars().all()
        return [m.to_domain() for m in results]

    def soft_delete(self, message_id: str) -> None:
        stmt = (
            update(ChatMessageModel)
            .where(ChatMessageModel.id == message_id)
            .values(is_deleted=True)
        )
        self.db.execute(stmt)
        self.db.flush()