from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.document import Document


class AbstractDocumentRepository(ABC):

    @abstractmethod
    def create(self, document: Document) -> Document:
        pass

    @abstractmethod
    def get_by_id(self, document_id: str) -> Optional[Document]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: str) -> List[Document]:
        pass

    @abstractmethod
    def get_by_hash(
        self,
        user_id: str,
        content_hash: str,
    ) -> Optional[Document]:
        pass