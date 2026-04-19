from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.db.base import Base
from app.infrastructure.db.mixins import SoftDeleteMixin, TimestampMixin
from app.domain.document import Document


class DocumentModel(Base, SoftDeleteMixin, TimestampMixin):
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
            created_at=self.created_at,
            updated_at=self.updated_at
        )