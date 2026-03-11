from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.chat_message import ChatMessage


class AbstractChatMessageRepository(ABC):

    @abstractmethod
    def create(self, message: ChatMessage) -> ChatMessage:
        """Persist new message."""
        pass

    @abstractmethod
    def get_by_id(self, message_id: str) -> Optional[ChatMessage]:
        """Fetch message by id."""
        pass

    @abstractmethod
    def get_by_session(self, session_id: str) -> List[ChatMessage]:
        """Fetch messages in chronological order."""
        pass

    @abstractmethod
    def soft_delete(self, message_id: str) -> None:
        """Soft delete message."""
        pass