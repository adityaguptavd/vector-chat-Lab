from pydantic import BaseModel

class StreamRequest(BaseModel):
    content: str