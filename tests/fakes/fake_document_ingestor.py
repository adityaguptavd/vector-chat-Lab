from app.domain.core.document_ingestor import AbstractDocumentIngestor


class FakeDocumentIngestor(AbstractDocumentIngestor):

    def __init__(self) -> None:
        self.calls = []

    def ingest(
        self,
        user_id: str,
        document_id: str,
        content: str,
    ) -> None:
        self.calls.append(
            {
                "user_id": user_id,
                "document_id": document_id,
                "content": content,
            }
        )