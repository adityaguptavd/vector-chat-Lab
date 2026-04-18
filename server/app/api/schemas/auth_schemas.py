from app.api.schemas.base import StrictBaseModel


class RegisterRequest(StrictBaseModel):
    email: str
    password: str
    full_name: str


class LoginRequest(StrictBaseModel):
    email: str
    password: str


class AuthResponse(StrictBaseModel):
    access_token: str
    user_id: str