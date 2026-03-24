from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.chat_session import ChatSession


class AbstractChatSessionRepository(ABC):

    @abstractmethod
    def create(self, session: ChatSession) -> ChatSession:
        """Persist a new chat session."""
        pass

    @abstractmethod
    def get_by_id(self, session_id: str) -> Optional[ChatSession]:
        """Fetch session by ID."""
        pass

    @abstractmethod
    def get_by_user(self, user_id: str) -> List[ChatSession]:
        """Fetch all sessions belonging to a user (latest first handled in infra)."""
        pass

    @abstractmethod
    def update(self, session: ChatSession) -> ChatSession:
        """Persist updates (archive/title/touch)."""
        pass