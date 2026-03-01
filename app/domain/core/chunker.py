from abc import ABC, abstractmethod
from typing import List


class AbstractChunker(ABC):

    @abstractmethod
    def chunk(self, content: str) -> List[str]:
        pass