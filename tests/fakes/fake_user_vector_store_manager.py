from app.domain.vector.user_vector_store_manager import (
    AbstractUserVectorStoreManager,
)
from app.domain.vector.vector_store import AbstractVectorStore
from tests.fakes.fake_vector_store import FakeVectorStore


class FakeUserVectorStoreManager(AbstractUserVectorStoreManager):

    def __init__(self) -> None:
        self.stores = {}

    def get_store(self, user_id: str) -> AbstractVectorStore:
        if user_id not in self.stores:
            self.stores[user_id] = FakeVectorStore()
        return self.stores[user_id]