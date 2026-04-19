from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.chat_session import ChatSession
from .base_repository import BaseRepository
from app.domain.repositories.chat_session_repository import (
    AbstractChatSessionRepository,
)
from app.infrastructure.db.models.chat_session_model import ChatSessionModel


class ChatSessionRepository(
    BaseRepository[ChatSessionModel],
    AbstractChatSessionRepository
):

    def __init__(self, db_session: Session):
        super().__init__(db_session, ChatSessionModel)

    def create(self, session: ChatSession) -> ChatSession:
        model = ChatSessionModel.from_domain(session)
        saved = super().create(model)
        return saved.to_domain()

    def get_by_id(
        self,
        session_id: str,
        include_deleted: bool = False
    ) -> Optional[ChatSession]:

        model = super().get_by_id(session_id, include_deleted)
        return model.to_domain() if model else None

    def get_by_user(self, user_id: str) -> List[ChatSession]:

        stmt = select(self.model)

        stmt = self._apply_filters(stmt, {
            "user_id": user_id,
            "is_archived": False
        })

        stmt = self._apply_not_deleted(stmt)
        stmt = self._apply_ordering(stmt, "-last_activity_at")

        results = self._execute(stmt)

        return [m.to_domain() for m in results]

    def get_archived_by_user(self, user_id: str) -> List[ChatSession]:

        stmt = select(self.model)

        stmt = self._apply_filters(stmt, {
            "user_id": user_id,
            "is_archived": True
        })

        stmt = self._apply_not_deleted(stmt)
        stmt = self._apply_ordering(stmt, "-last_activity_at")

        results = self._execute(stmt)

        return [m.to_domain() for m in results]

    def update(self, session: ChatSession) -> ChatSession:

        self.update_fields(
            session.id,
            {
                "title": session.title,
                "is_archived": session.is_archived,
                "last_activity_at": session.last_activity_at
            }
        )

        # returns domain directly
        updated = self.get_by_id(session.id, include_deleted=True)

        return updated