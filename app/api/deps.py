from typing import Generator
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.security.bcrypt_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_token_provider import JwtTokenProvider
from app.application.services.user_service import UserService
from app.application.services.chat_service import ChatService
from app.domain.unit_of_work import AbstractUnitOfWork
from app.domain.security.password_hasher import AbstractPasswordHasher
from app.domain.security.token_provider import AbstractTokenProvider
from app.core.config import settings
from app.domain.exceptions import InvalidToken
from fastapi import Depends
from app.domain.user import User
from app.core.logging.context import user_id_ctx

def _get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_uow(db: Session = Depends(_get_db)) -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(db)


def get_password_hasher() -> AbstractPasswordHasher:
    return BcryptPasswordHasher()

def get_token_provider() -> AbstractTokenProvider:
    return JwtTokenProvider(secret_key=settings.JWT_SECRET)

def get_bearer_token(authorization: str | None = Header(default=None, include_in_schema=False)) -> str:
    if not authorization:
        raise InvalidToken()

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise InvalidToken()

    return token

def get_user_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    password_hasher: AbstractPasswordHasher = Depends(get_password_hasher),
    token_provider: AbstractTokenProvider = Depends(get_token_provider),
) -> UserService:

    return UserService(
        uow=uow,
        password_hasher=password_hasher,
        token_provider=token_provider,
    )

async def get_current_user(
    token: str = Depends(get_bearer_token),
    user_service: UserService = Depends(get_user_service),
) -> User:

    user = user_service.get_user_from_token(token)

    # inject into logging context
    user_id_ctx.set(user.id)

    return user

def get_chat_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> ChatService:
    return ChatService(uow)