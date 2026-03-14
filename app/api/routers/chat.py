from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_chat_service
from app.application.services.chat_service import ChatService
from app.domain.user import User
from app.core.responses import ResponseBuilder


router = APIRouter(prefix="/chat", tags=["Chat"])


# ---------------- SESSION ----------------


@router.post("/sessions")
def create_session(
    title: str | None = None,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    payload = service.create_session(user.id, title)

    return ResponseBuilder.success(message="Chat session created", status_code=201, data=payload.model_dump(mode="json"))


@router.get("/sessions")
def list_sessions(
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    payload = service.list_sessions(user.id)

    return ResponseBuilder.success(message="Chat sessions retrieved", data=[p.model_dump(mode="json") for p in payload])


# ---------------- MESSAGE ----------------


@router.post("/{session_id}/messages")
async def send_message(
    session_id: str,
    content: str,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    payload = await service.add_user_message_and_generate(
        user_id=user.id,
        session_id=session_id,
        content=content
    )

    return ResponseBuilder.success(message="Message sent and received", status_code=201, data=payload)



@router.get("/{session_id}/messages")
def list_messages(
    session_id: str,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    payload = service.list_messages(user.id, session_id)

    return ResponseBuilder.success(message="All messages fetched", data=[p.model_dump(mode="json") for p in payload])