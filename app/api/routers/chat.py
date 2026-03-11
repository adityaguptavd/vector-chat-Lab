from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_chat_service
from app.application.services.chat_service import ChatService
from app.domain.user import User
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.domain.chat_message import MessageRole


router = APIRouter(prefix="/chat", tags=["Chat"])


# ---------------- SESSION ----------------


@router.post("/sessions")
def create_session(
    title: str | None = None,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    return service.create_session(user.id, title)


@router.get("/sessions")
def list_sessions(
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    return service.list_sessions(user.id)


# ---------------- MESSAGE ----------------


@router.post("/{session_id}/messages")
def send_message(
    session_id: str,
    content: str,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    return service.send_message(
        user_id=user.id,
        session_id=session_id,
        content=content,
        role=MessageRole.USER,
    )


@router.get("/{session_id}/messages")
def list_messages(
    session_id: str,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    return service.list_messages(user.id, session_id)