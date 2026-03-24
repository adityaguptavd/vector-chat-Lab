from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from app.core.utils.id_generator import IDGenerator


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass(slots=True)
class ChatMessage:
    id: str
    session_id: str
    role: MessageRole
    content: str
    created_at: datetime
    is_deleted: bool = False

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        role: MessageRole,
        content: str,
    ) -> "ChatMessage":

        if not content.strip():
            raise ValueError("Message content cannot be empty")

        return cls(
            id=IDGenerator.generate(prefix="Msg", time_sortable=True),
            session_id=session_id,
            role=role,
            content=content,
            created_at=_utcnow(),
            is_deleted=False,
        )

    def soft_delete(self) -> None:
        self.is_deleted = True