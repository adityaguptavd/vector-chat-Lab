from pydantic import BaseModel
from datetime import datetime
from app.domain.chat_message import MessageRole


class ChatSessionResult(BaseModel):
    id: str
    title: str | None
    created_at: datetime
    updated_at: datetime
    is_archived: bool

    class Config:
        from_attributes = True

class ChatMessageResult(BaseModel):
    id: str
    session_id: str
    role: MessageRole
    content: str
    created_at: datetime

    class Config:
        from_attributes = True