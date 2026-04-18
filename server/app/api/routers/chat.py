from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse

from app.api.deps import get_current_user, get_chat_service
from app.api.schemas.chat_schemas import StreamRequest
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
) -> JSONResponse:
    payload = service.create_session(user.id, title)

    return ResponseBuilder.success(message="Chat session created", status_code=201, data=payload.model_dump(mode="json"))


@router.get("/sessions")
def list_sessions(
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> JSONResponse:
    payload = service.list_sessions(user.id)

    return ResponseBuilder.success(message="Chat sessions retrieved", data=[p.model_dump(mode="json") for p in payload])

@router.get("/sessions/archived")
def list_sessions(
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> JSONResponse:
    payload = service.list_archived_sessions(user.id)

    return ResponseBuilder.success(message="Chat sessions retrieved", data=[p.model_dump(mode="json") for p in payload])


# ---------------- MESSAGE ----------------


@router.post("/{session_id}/messages")
async def send_message(
    session_id: str,
    content: str,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> JSONResponse:
    payload = await service.add_user_message_and_generate(
        user_id=user.id,
        session_id=session_id,
        content=content
    )

    return ResponseBuilder.success(message="Message sent and received", status_code=201, data=[p.model_dump(mode="json") for p in payload])



@router.get("/{session_id}/messages")
def list_messages(
    session_id: str,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> JSONResponse:
    payload = service.list_messages(user.id, session_id)

    return ResponseBuilder.success(message="All messages fetched", data=[p.model_dump(mode="json") for p in payload])

@router.get("/{session_id}/stream")
async def stream_chat(
    session_id: str,
    content: str,
    service: ChatService = Depends(get_chat_service),
    user: User = Depends(get_current_user)
) -> StreamingResponse:

    # validate stream request and get session
    session = service.get_or_create_session(user_id=user.id, session_id=session_id)
    
    user_msg = service.store_user_message(user_id=user.id, session=session, content=content)

    return StreamingResponse(
        service.stream_message(session=session, user_msg=user_msg, content=content, user_id=user.id),
        media_type="text/event-stream"
    )


@router.post("/{session_id}/stream")
async def stream_chat(
    session_id: str,
    body: StreamRequest,
    service: ChatService = Depends(get_chat_service),
    user: User = Depends(get_current_user)
) -> StreamingResponse:

    content = body.content

    session = service.get_or_create_session(user_id=user.id, session_id=session_id)
    
    user_msg = service.store_user_message(
        user_id=user.id,
        session=session,
        content=content
    )

    return StreamingResponse(
        service.stream_message(
            session=session,
            user_msg=user_msg,
            content=content,
            user_id=user.id
        ),
        media_type="text/event-stream"
    )

@router.patch("/sessions/{session_id}/archive")
def archive_session(
    session_id: str,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> JSONResponse:

    payload = service.archive_session(user.id, session_id)

    return ResponseBuilder.success(
        message="Chat session archived",
        data=payload.model_dump(mode="json")
    )


@router.patch("/sessions/{session_id}/unarchive")
def unarchive_session(
    session_id: str,
    user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> JSONResponse:

    payload = service.unarchive_session(user.id, session_id)

    return ResponseBuilder.success(
        message="Chat session unarchived",
        data=payload.model_dump(mode="json")
    )