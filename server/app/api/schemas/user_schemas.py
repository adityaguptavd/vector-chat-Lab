from app.api.schemas.base import StrictBaseModel

class UserMeResponse(StrictBaseModel):
    user_id: str
    email: str
    full_name: str | None