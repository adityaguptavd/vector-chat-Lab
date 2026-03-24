from pathlib import Path

from app.domain.vector.user_vector_store_manager import AbstractUserVectorStoreManager
from app.infrastructure.vector.faiss_vector_store import FAISSVectorStore
from app.domain.vector.vector_store import AbstractVectorStore


class FAISSUserVectorStoreManager(AbstractUserVectorStoreManager):

    def __init__(self, base_path: str, embedding_dim: int) -> None:
        self._base_path = Path(base_path or "/app/vector_store")
        self._base_path.mkdir(parents=True, exist_ok=True)
        self._embedding_dim = embedding_dim

    def get_store(self, user_id: str) -> AbstractVectorStore:
        user_path = self._base_path / user_id
        return FAISSVectorStore(user_path, self._embedding_dim)