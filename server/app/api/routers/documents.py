from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from app.api.deps import get_current_user, get_document_service
from app.application.services.document_service import DocumentService
from app.domain.user import User
from app.core.responses import ResponseBuilder


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):

    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")

    content = await file.read()

    document = service.upload_document(
        user_id=user.id,
        filename=file.filename,
        content=content,
    )

    return ResponseBuilder.success(
        message="Document uploaded successfully",
        status_code=201,
        data=document.model_dump(mode="json")
    )

@router.get("/")
async def list_documents(
    user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):
    documents = service.list_documents(user.id)

    return ResponseBuilder.success(
        message="Documents fetched successfully",
        data=[doc.model_dump(mode="json") for doc in documents],
    )