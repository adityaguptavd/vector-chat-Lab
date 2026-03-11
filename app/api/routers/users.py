from fastapi import APIRouter, Depends
from app.domain.user import User
from app.api.deps import get_current_user
from app.api.schemas.user_schemas import UserMeResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)) -> UserMeResponse:
    return UserMeResponse(
        id=current_user.id,
        email=current_user.email
    )