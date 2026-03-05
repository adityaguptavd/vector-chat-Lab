from pathlib import Path
from typing import List
import json

import faiss
import numpy as np

from app.domain.vector.vector_store import AbstractVectorStore
from app.infrastructure.vector.schemas.vector_document import VectorDocument

class FAISSVectorStore(AbstractVectorStore):

    def __init__(self, path: Path, embedding_dim: int) -> None:
        self._path = path
        self._embedding_dim = embedding_dim
        self._index_path = path / "index.faiss"
        self._meta_path = path / "documents.json"

        self._index: faiss.Index
        self._documents: List[VectorDocument] = []

        self._load_or_initialize()

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def _load_or_initialize(self) -> None:
        self._path.mkdir(parents=True, exist_ok=True)

        if self._index_path.exists():
            self._index = faiss.read_index(str(self._index_path))
            self._load_documents()

            # Dimension safety validation
            if self._index.d != self._embedding_dim:
                raise ValueError(
                    f"Embedding dimension mismatch. "
                    f"Index dim={self._index.d}, expected={self._embedding_dim}"
                )
        else:
            self._index = faiss.IndexFlatIP(self._embedding_dim)
            self._documents = []

    def _load_documents(self) -> None:
        if self._meta_path.exists():
            with open(self._meta_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                self._documents = [
                    VectorDocument(**item) for item in raw
                ]
        else:
            self._documents = []

    def _persist(self) -> None:
        faiss.write_index(self._index, str(self._index_path))

        with open(self._meta_path, "w", encoding="utf-8") as f:
            json.dump(
                [doc.model_dump() for doc in self._documents],
                f,
                indent=2,
                ensure_ascii=False,
            )

    # ----------------------------------
    # Interface Implementation
    # ----------------------------------

    def add_documents(
        self,
        documents: List[VectorDocument],
    ) -> None:

        if not documents:
            return

        embeddings = []

        for doc in documents:
            if len(doc.embedding) != self._embedding_dim:
                raise ValueError(
                    f"Embedding dimension mismatch. "
                    f"Expected {self._embedding_dim}, "
                    f"got {len(doc.embedding)}"
                )

            embeddings.append(doc.embedding)
            self._documents.append(doc)

        np_embeddings = np.array(embeddings).astype("float32")
        self._index.add(np_embeddings)

        self._persist()

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
    ) -> List[VectorDocument]:

        if len(query_embedding) != self._embedding_dim:
            raise ValueError(
                f"Query embedding dimension mismatch. "
                f"Expected {self._embedding_dim}, "
                f"got {len(query_embedding)}"
            )

        if self._index.ntotal == 0:
            return []

        query = np.array([query_embedding]).astype("float32")
        distances, indices = self._index.search(query, top_k)

        results: List[VectorDocument] = []

        for idx in indices[0]:
            if idx == -1:
                continue

            results.append(self._documents[idx])

        return results