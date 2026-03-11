from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base
from app.domain.chat_message import ChatMessage, MessageRole


class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    session_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("chat_sessions.id"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    @classmethod
    def from_domain(cls, message: ChatMessage) -> "ChatMessageModel":
        return cls(
            id=message.id,
            session_id=message.session_id,
            role=message.role.value,
            content=message.content,
            created_at=message.created_at,
            is_deleted=message.is_deleted,
        )

    def to_domain(self) -> ChatMessage:
        return ChatMessage(
            id=self.id,
            session_id=self.session_id,
            role=MessageRole(self.role),
            content=self.content,
            created_at=self.created_at,
            is_deleted=self.is_deleted,
        )