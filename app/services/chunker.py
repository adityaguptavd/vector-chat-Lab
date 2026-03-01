from app.domain.services.chunker import AbstractChunker
from typing import List

class SimpleChunker(AbstractChunker):

    def __init__(self, chunk_size: int = 500) -> None:
        self.chunk_size = chunk_size

    def chunk(self, content: str) -> List[str]:
        return [
            content[i : i + self.chunk_size]
            for i in range(0, len(content), self.chunk_size)
        ]