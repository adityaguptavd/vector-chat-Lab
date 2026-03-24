from pydantic import BaseModel, Field
from typing import Dict, Any, List


class VectorDocument(BaseModel):
    document_id: str
    chunk_id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any] = Field(default_factory=dict)