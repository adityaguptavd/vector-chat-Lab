from typing import List
from app.domain.vector.embedder import AbstractEmbedder


class FakeEmbedder(AbstractEmbedder):

    def embed(self, texts: List[str]) -> List[List[float]]:
        # Deterministic embedding: length of string
        return [[float(len(text))] for text in texts]