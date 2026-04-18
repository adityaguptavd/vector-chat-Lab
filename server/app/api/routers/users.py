from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.domain.user import User
from app.api.deps import get_current_user
from app.api.schemas.user_schemas import UserMeResponse
from app.core.responses import ResponseBuilder

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)) -> JSONResponse:
    payload = UserMeResponse(
        user_id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name
    )
    return ResponseBuilder.success(
        message="User retrieved successfully",
        data=payload.model_dump(mode="json")
    )