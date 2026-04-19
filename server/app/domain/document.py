from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from app.core.utils.id_generator import IDGenerator


@dataclass(slots=True)
class Document:
    id: str
    user_id: str
    filename: str
    content_hash: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        *,
        user_id: str,
        filename: str,
        content_hash: str,
    ) -> "Document":
        return cls(
            id=IDGenerator.generate(prefix="doc"),
            user_id=user_id,
            filename=filename,
            content_hash=content_hash,
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "content_hash": self.content_hash,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }