from app.domain.document import Document
from app.domain.unit_of_work import AbstractUnitOfWork
from app.domain.core.document_ingestor import AbstractDocumentIngestor
from app.domain.core.content_hasher import AbstractContentHasher
from app.application.dto.document import DocumentResult

from typing import List


class DocumentService:

    def __init__(
        self,
        uow: AbstractUnitOfWork,
        ingestor: AbstractDocumentIngestor,
        content_hasher: AbstractContentHasher,
    ) -> None:
        self.uow = uow
        self.ingestor = ingestor
        self.content_hasher = content_hasher

    def upload_document(
        self,
        user_id: str,
        filename: str,
        content: bytes,
    ) -> DocumentResult:

        content_hash = self.content_hasher.hash(content)

        with self.uow:
            existing = self.uow.document_repo.get_by_hash(
                user_id,
                content_hash,
            )

            if existing:
                self.ingestor.ingest(
                    user_id=user_id,
                    document_id=existing.id,
                    content_bytes=content,
                    filename=filename,
                )
                return DocumentResult.model_validate(existing)

            document = Document.create(
                user_id=user_id,
                filename=filename,
                content_hash=content_hash,
            )

            created = self.uow.document_repo.create(document)

        # OUTSIDE TX
        self.ingestor.ingest(
            user_id=user_id,
            document_id=created.id,
            content_bytes=content,
            filename=filename,
        )

        return DocumentResult.model_validate(created)
    
    def list_documents(self, user_id: str) -> List[DocumentResult]:
            with self.uow:
                documents = self.uow.document_repo.get_by_user(user_id)

            return [
                DocumentResult.model_validate(doc)
                for doc in documents
            ]
    