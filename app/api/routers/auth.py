from fastapi import APIRouter, Depends

from app.api.deps import get_user_service
from app.api.schemas.auth_schemas import RegisterRequest, LoginRequest, AuthResponse
from app.application.services.user_service import UserService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=AuthResponse)
def register(
    data: RegisterRequest,
    service: UserService = Depends(get_user_service),
):
    user = service.register_user(data.email, data.password)

    # Immediately issue token (better UX)
    result = service.login_user(data.email, data.password)

    return AuthResponse(
        access_token=result.access_token,
        user_id=result.user_id
    )


@router.post("/login", response_model=AuthResponse)
def login(
    data: LoginRequest,
    service: UserService = Depends(get_user_service),
):
    result = service.login_user(data.email, data.password)

    return AuthResponse(
        access_token=result.access_token,
        user_id=result.user_id
    )