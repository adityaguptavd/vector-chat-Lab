from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.document import Document
from app.domain.repositories.document_repository import (
    AbstractDocumentRepository,
)
from app.infrastructure.db.models.document_model import DocumentModel


class DocumentRepository(AbstractDocumentRepository):

    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, document: Document) -> Document:
        model = DocumentModel.from_domain(document)
        self.db.add(model)
        self.db.flush()
        return model.to_domain()

    def get_by_id(self, document_id: str) -> Optional[Document]:
        model = self.db.get(DocumentModel, document_id)
        return model.to_domain() if model else None

    def get_by_user(self, user_id: str) -> List[Document]:
        stmt = select(DocumentModel).where(
            DocumentModel.user_id == user_id
        )
        results = self.db.execute(stmt).scalars().all()
        return [model.to_domain() for model in results]

    def get_by_hash(
        self,
        user_id: str,
        content_hash: str,
    ) -> Optional[Document]:
        stmt = select(DocumentModel).where(
            DocumentModel.user_id == user_id,
            DocumentModel.content_hash == content_hash,
        )
        result = self.db.execute(stmt).scalar_one_or_none()
        return result.to_domain() if result else None