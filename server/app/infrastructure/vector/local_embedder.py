from typing import List, cast
import numpy as np
import numpy.typing as npt
from sentence_transformers import SentenceTransformer

from app.domain.vector.embedder import AbstractEmbedder


class LocalSentenceTransformerEmbedder(AbstractEmbedder):

    def __init__(self, model_name: str) -> None:
        self.model = SentenceTransformer(model_name)

    @property
    def dimension(self) -> int:
        dim = self.model.get_sentence_embedding_dimension()
        if dim is None:
            raise RuntimeError("Embedding dimension could not be determined.")
        return dim

    def embed(self, texts: List[str]) -> List[List[float]]:
        raw = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        array: npt.NDArray[np.float32] = np.asarray(raw, dtype=np.float32)

        result = array.tolist()

        return cast(List[List[float]], result)