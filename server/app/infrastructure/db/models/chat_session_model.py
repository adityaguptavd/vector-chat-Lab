from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.infrastructure.db.base import Base
from app.infrastructure.db.mixins import SoftDeleteMixin, TimestampMixin
from app.domain.chat_session import ChatSession


class ChatSessionModel(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str | None] = mapped_column(String, nullable=True)

    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    @classmethod
    def from_domain(cls, session: ChatSession) -> "ChatSessionModel":
        return cls(
            id=session.id,
            user_id=session.user_id,
            title=session.title,
            is_archived=session.is_archived,
            last_activity_at=session.last_activity_at
        )

    def to_domain(self) -> ChatSession:
        return ChatSession(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            is_archived=self.is_archived,
            created_at=self.created_at,
            updated_at=self.updated_at,
            last_activity_at=self.last_activity_at
        )