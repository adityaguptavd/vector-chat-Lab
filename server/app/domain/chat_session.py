from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from app.core.utils.id_generator import IDGenerator


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class ChatSession:
    id: str
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_archived: bool = False

    @classmethod
    def create(
        cls,
        *,
        user_id: str,
        title: Optional[str] = None,
    ) -> "ChatSession":
        now = _utcnow()
        return cls(
            id=IDGenerator.generate(prefix="ch"),
            user_id=user_id,
            title=title,
            created_at=now,
            updated_at=now,
            is_archived=False,
        )

    def archive(self) -> None:
        self.is_archived = True
        self.touch()

    def unarchive(self) -> None:
        self.is_archived = False
        self.touch()

    def touch(self) -> None:
        self.updated_at = _utcnow()