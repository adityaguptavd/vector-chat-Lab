from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.db.base import Base
from app.domain.user import User
from typing import Optional

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            password_hash=user.password_hash,
        )

    def to_domain(self) -> User:
        return User(
            id=self.id,
            full_name=self.full_name,
            email=self.email,
            password_hash=self.password_hash
        )
