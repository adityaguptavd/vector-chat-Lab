from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from app.core.utils.id_generator import IDGenerator
from app.domain.exceptions import BadRequestError

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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        role: MessageRole,
        content: str,
    ) -> "ChatMessage":

        if not content.strip():
            raise BadRequestError("Message content cannot be empty")

        return cls(
            id=IDGenerator.generate(prefix="Msg", time_sortable=True),
            session_id=session_id,
            role=role,
            content=content,
            created_at=None,
            updated_at=None
        )