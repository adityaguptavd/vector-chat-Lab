from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.deps import get_user_service
from app.api.schemas.auth_schemas import RegisterRequest, LoginRequest, AuthResponse
from app.application.services.user_service import UserService
from app.core.responses import ResponseBuilder


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=AuthResponse)
def register(
    data: RegisterRequest,
    service: UserService = Depends(get_user_service),
) -> JSONResponse:
    user = service.register_user(data.email, data.password, data.full_name)

    # Immediately issue token (better UX)
    result = service.login_user(data.email, data.password)

    payload = AuthResponse(
        access_token=result.access_token,
        user_id=result.user_id
    )

    return ResponseBuilder.success(message="User registered successfully", status_code=201, data=payload.model_dump(mode="json"))


@router.post("/login", response_model=AuthResponse)
def login(
    data: LoginRequest,
    service: UserService = Depends(get_user_service),
) -> JSONResponse:
    result = service.login_user(data.email, data.password)

    payload = AuthResponse(
        access_token=result.access_token,
        user_id=result.user_id
    )

    return ResponseBuilder.success(message="User logged in successfully", data=payload.model_dump(mode="json"))