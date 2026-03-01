from pydantic import BaseModel
from typing import Dict, Any, List


class VectorDocument(BaseModel):
    document_id: str
    chunk_id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any] = {}