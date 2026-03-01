from pathlib import Path

from app.domain.vector.user_vector_store_manager import AbstractUserVectorStoreManager
from app.vector.faiss_vector_store import FAISSVectorStore


class FAISSUserVectorStoreManager(AbstractUserVectorStoreManager):

    def __init__(self, base_path: Path, embedding_dim: int):
        self._base_path = base_path
        self._embedding_dim = embedding_dim

    def get_store(self, user_id: str) -> FAISSVectorStore:
        user_path = self._base_path / user_id
        return FAISSVectorStore(user_path, self._embedding_dim)