from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from app.domain.user import User


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
        )

    def to_domain(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            password_hash=self.password_hash
        )