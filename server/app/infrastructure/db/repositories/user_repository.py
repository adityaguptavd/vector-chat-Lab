from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domain.user import User
from app.domain.exceptions import UserAlreadyExists
from app.domain.repositories.user_repository import AbstractUserRepository

from app.infrastructure.db.models.user_model import UserModel
from .base_repository import BaseRepository


class UserRepository(
    BaseRepository[UserModel],
    AbstractUserRepository
):

    def __init__(self, db_session: Session):
        super().__init__(db_session, UserModel)

    # ------------------------
    # 🟢 CREATE
    # ------------------------
    def create(self, user: User) -> User:
        model = UserModel.from_domain(user)

        try:
            saved = super().create(model)
        except IntegrityError as exc:
            raise UserAlreadyExists(
                f"User with email '{user.email}' already exists"
            ) from exc

        return saved.to_domain()

    # ------------------------
    # 🔍 GET BY ID
    # ------------------------
    def get_by_id(
        self,
        user_id: str,
        include_deleted: bool = False
    ) -> Optional[User]:

        model = super().get_by_id(user_id, include_deleted)
        return model.to_domain() if model else None

    # ------------------------
    # 📧 GET BY EMAIL
    # ------------------------
    def get_by_email(self, email: str) -> Optional[User]:

        stmt = select(self.model)

        stmt = self._apply_filters(stmt, {
            "email": email
        })

        stmt = self._apply_not_deleted(stmt)

        model = self._execute_one(stmt)

        return model.to_domain() if model else None

    # ------------------------
    # 🔢 EXISTS BY EMAIL
    # ------------------------
    def exists_by_email(self, email: str) -> bool:
        return self._exists({
            "email": email
        })