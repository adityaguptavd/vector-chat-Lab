from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from app.domain.user import User
from app.domain.document import Document

# Model - 1: User
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

# Model - 2: Document
class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    filename: Mapped[str] = mapped_column(String, nullable=False)

    content_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    @classmethod
    def from_domain(cls, document: Document) -> "DocumentModel":
        return cls(
            id=document.id,
            user_id=document.user_id,
            filename=document.filename,
            content_hash=document.content_hash,
        )

    def to_domain(self) -> Document:
        return Document(
            id=self.id,
            user_id=self.user_id,
            filename=self.filename,
            content_hash=self.content_hash,
        )