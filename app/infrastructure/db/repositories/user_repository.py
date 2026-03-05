from app.infrastructure.db.models.user_model import UserModel
from app.domain.repositories.user_repository import AbstractUserRepository
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.domain.exceptions import UserAlreadyExists

from app.domain.user import User

class UserRepository(AbstractUserRepository):

    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, user: User) -> User:
        model = UserModel.from_domain(user)
        self.db.add(model)

        try:
            self.db.flush()
        except IntegrityError as exc:
            raise UserAlreadyExists(
                f"User with email '{user.email}' already exists"
            ) from exc

        return model.to_domain()
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        model = self.db.get(UserModel, user_id)
        return model.to_domain() if model else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = self.db.execute(stmt).scalar_one_or_none()

        return result.to_domain() if result else None

    def exists_by_email(self, email: str) -> bool:
        stmt = select(func.count()).select_from(UserModel).where(
            UserModel.email == email
        )
        count = self.db.execute(stmt).scalar_one()
        return count > 0