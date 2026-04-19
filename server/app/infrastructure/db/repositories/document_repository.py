from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.document import Document
from app.domain.repositories.document_repository import (
    AbstractDocumentRepository,
)
from app.infrastructure.db.models.document_model import DocumentModel
from .base_repository import BaseRepository


class DocumentRepository(
    BaseRepository[DocumentModel],
    AbstractDocumentRepository
):

    def __init__(self, db_session: Session):
        super().__init__(db_session, DocumentModel)

    # ------------------------
    # 🟢 CREATE
    # ------------------------
    def create(self, document: Document) -> Document:
        model = DocumentModel.from_domain(document)
        saved = super().create(model)
        return saved.to_domain()

    # ------------------------
    # 🔍 GET BY ID
    # ------------------------
    def get_by_id(
        self,
        document_id: str,
        include_deleted: bool = False
    ) -> Optional[Document]:

        model = super().get_by_id(document_id, include_deleted)
        return model.to_domain() if model else None

    # ------------------------
    # 📄 GET BY USER
    # ------------------------
    def get_by_user(self, user_id: str) -> List[Document]:

        stmt = select(self.model)

        stmt = self._apply_filters(stmt, {
            "user_id": user_id
        })

        stmt = self._apply_not_deleted(stmt)

        stmt = self._apply_ordering(stmt, order_by="-updated_at")

        results = self._execute(stmt)

        return [m.to_domain() for m in results]

    # ------------------------
    # 🔍 GET BY HASH
    # ------------------------
    def get_by_hash(
        self,
        user_id: str,
        content_hash: str,
    ) -> Optional[Document]:

        stmt = select(self.model)

        stmt = self._apply_filters(stmt, {
            "user_id": user_id,
            "content_hash": content_hash
        })

        stmt = self._apply_not_deleted(stmt)

        model = self._execute_one(stmt)

        return model.to_domain() if model else None