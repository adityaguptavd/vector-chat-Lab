from app.api.schemas.base import StrictBaseModel

class UserMeResponse(StrictBaseModel):
    id: str
    email: str