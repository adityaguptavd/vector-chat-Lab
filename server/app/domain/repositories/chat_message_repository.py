from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.chat_message import ChatMessage


class AbstractChatMessageRepository(ABC):

    @abstractmethod
    def create(self, message: ChatMessage) -> ChatMessage:
        pass

    @abstractmethod
    def get_by_id(
        self,
        message_id: str,
        include_deleted: bool = False
    ) -> Optional[ChatMessage]:
        pass

    @abstractmethod
    def get_by_session(
        self,
        session_id: str,
        *,
        page: int = 1,
        limit: int = 50
    ) -> List[ChatMessage]:
        pass

    @abstractmethod
    def soft_delete(self, message_id: str) -> None:
        pass