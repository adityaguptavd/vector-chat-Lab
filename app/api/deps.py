from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.security.bcrypt_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_token_provider import JwtTokenProvider
from fastapi import Depends
from app.application.services.user_service import UserService
from app.domain.unit_of_work import AbstractUnitOfWork
from app.domain.security.password_hasher import AbstractPasswordHasher
from app.domain.security.token_provider import AbstractTokenProvider
from app.core.config import settings

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