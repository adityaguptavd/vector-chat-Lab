from app.domain.document import Document
from app.domain.unit_of_work import AbstractUnitOfWork
from app.domain.services.document_ingestor import AbstractDocumentIngestor
from app.domain.services.content_hasher import AbstractContentHasher


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
    ) -> Document:

        content_hash = self.content_hasher.hash(content)

        with self.uow:
            existing = self.uow.document_repo.get_by_hash(
                user_id,
                content_hash,
            )

            if existing:
                return existing

            document = Document.create(
                user_id=user_id,
                filename=filename,
                content_hash=content_hash,
            )

            created = self.uow.document_repo.create(document)

            self.ingestor.ingest(
                user_id=user_id,
                document_id=created.id,
                content=content.decode(),
            )

            return created