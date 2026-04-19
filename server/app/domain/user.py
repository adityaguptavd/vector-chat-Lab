from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from app.core.utils.id_generator import IDGenerator


@dataclass(slots=True)
class User:
    id: str
    email: str
    password_hash: str
    full_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        *,
        email: str,
        password_hash: str,
        full_name: Optional[str] = None,
    ) -> "User":
        return cls(
            id=IDGenerator.generate(prefix="usr"),
            email=email,
            password_hash=password_hash,
            full_name=full_name,
        )

    def to_dict(self) -> dict[str, Optional[str]]:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }