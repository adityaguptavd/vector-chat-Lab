from abc import ABC, abstractmethod


class AbstractDocumentIngestor(ABC):

    @abstractmethod
    def ingest(
        self,
        user_id: str,
        document_id: str,
        content: str,
    ) -> None:
        pass