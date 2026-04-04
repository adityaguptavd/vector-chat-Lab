from app.domain.core.document_ingestor import AbstractDocumentIngestor
from app.domain.vector.user_vector_store_manager import (
    AbstractUserVectorStoreManager,
)
from app.domain.vector.embedder import AbstractEmbedder
from app.domain.core.chunker import AbstractChunker
from app.infrastructure.vector.schemas.vector_document import VectorDocument
from app.domain.exceptions import UnsupportedFileType
from io import BytesIO
from pypdf import PdfReader
import mimetypes

from app.core.logging.logger import LoggingManager

logger = LoggingManager.get_logger("document_ingestor_service")

class SimpleDocumentIngestor(AbstractDocumentIngestor):

    def __init__(
        self,
        user_vector_manager: AbstractUserVectorStoreManager,
        embedder: AbstractEmbedder,
        chunker: AbstractChunker
    ) -> None:
        self.user_vector_manager = user_vector_manager
        self.embedder = embedder
        self.chunker = chunker

    def _parse_bytes(self, content_bytes: bytes, filename: str) -> str:

        logger.info("INGESTOR_VERSION", extra={"version": "v2_mimetypes"})

        filename = filename.lower().strip()

        mime, _ = mimetypes.guess_type(filename)

        if mime == "application/pdf":
            reader = PdfReader(BytesIO(content_bytes))
            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )
            return text

        elif mime in ["text/plain", "text/markdown"]:
            return content_bytes.decode("utf-8", errors="ignore")

        else:
            raise UnsupportedFileType(message="Only pdf, text and markdown files are allowed")

    def ingest(
        self,
        user_id: str,
        document_id: str,
        content_bytes: bytes,
        filename: str
    ) -> None:
        store = self.user_vector_manager.get_store(user_id)

        text = self._parse_bytes(content_bytes, filename)

        chunks = self.chunker.chunk(text)

        embeddings = self.embedder.embed(chunks)

        documents = []

        for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            documents.append(
                VectorDocument(
                    document_id=document_id,
                    chunk_id=f"{document_id}_chunk_{idx}",
                    content=chunk_text,
                    embedding=embedding,
                    metadata={ "filename": filename },
                )
            )

        store.add_documents(documents)