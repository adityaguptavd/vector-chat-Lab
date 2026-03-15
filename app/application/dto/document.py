from pydantic import BaseModel
from datetime import datetime


class DocumentResult(BaseModel):
    id: str
    filename: str

    class Config:
        from_attributes = True