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
    last_activity_at: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
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
            is_archived=False,
            last_activity_at=now
        )

    def archive(self) -> None:
        self.is_archived = True
        self.update_last_activity()

    def unarchive(self) -> None:
        self.is_archived = False
        self.update_last_activity()

    def update_last_activity(self, updated_time: Optional[datetime] = None) -> None:
        self.last_activity_at = updated_time or _utcnow()