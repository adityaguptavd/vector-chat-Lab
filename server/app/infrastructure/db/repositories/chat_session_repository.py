from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.chat_session import ChatSession
from app.domain.repositories.chat_session_repository import (
    AbstractChatSessionRepository,
)
from app.infrastructure.db.models.chat_session_model import ChatSessionModel


class ChatSessionRepository(AbstractChatSessionRepository):

    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, session: ChatSession) -> ChatSession:
        model = ChatSessionModel.from_domain(session)
        self.db.add(model)
        self.db.flush()
        return model.to_domain()

    def get_by_id(self, session_id: str) -> Optional[ChatSession]:
        model = self.db.get(ChatSessionModel, session_id)
        return model.to_domain() if model else None

    def get_by_user(self, user_id: str) -> List[ChatSession]:
        stmt = (
            select(ChatSessionModel)
            .where(
                ChatSessionModel.user_id == user_id,
                ChatSessionModel.is_archived.is_(False)
            )
            .order_by(ChatSessionModel.updated_at.desc())
        )
        results = self.db.execute(stmt).scalars().all()
        return [model.to_domain() for model in results]
    
    def get_archived_by_user(self, user_id: str) -> List[ChatSession]:
        stmt = (
            select(ChatSessionModel)
            .where(
                ChatSessionModel.user_id == user_id,
                ChatSessionModel.is_archived.is_(True)
            )
            .order_by(ChatSessionModel.updated_at.desc())
        )

        results = self.db.execute(stmt).scalars().all()
        return [model.to_domain() for model in results]

    def update(self, session: ChatSession) -> ChatSession:
        model = self.db.get(ChatSessionModel, session.id)
        if not model:
            raise ValueError("ChatSession not found")

        model.title = session.title
        model.updated_at = session.updated_at
        model.is_archived = session.is_archived

        self.db.flush()
        return model.to_domain()