from app.domain.unit_of_work import AbstractUnitOfWork
from app.domain.security.password_hasher import AbstractPasswordHasher
from app.domain.security.token_provider import AbstractTokenProvider
from app.domain.user import User
from app.domain.exceptions import UserAlreadyExists, InvalidCredentials, InvalidToken
from app.domain.security.token_provider import TokenPayload
from app.schemas.dto import AuthResult

class UserService:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        password_hasher: AbstractPasswordHasher,
        token_provider: AbstractTokenProvider
    ) -> None:
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_provider = token_provider

    def register_user(self, email: str, raw_password: str) -> User:
        with self.uow:
            if self.uow.user_repo.exists_by_email(email):
                raise UserAlreadyExists(
                    f"User with email '{email}' already exists"
                )

            hashed = self.password_hasher.hash(raw_password)

            user = User.create(
                email=email,
                password_hash=hashed,
            )

            created = self.uow.user_repo.create(user)
            return created
        
    def login_user(self, email: str, raw_password: str) -> AuthResult:
        with self.uow:
            user = self.uow.user_repo.get_by_email(email)

            if user is None:
                raise InvalidCredentials("Invalid email or password.")

            is_valid = self.password_hasher.verify(
                raw_password,
                user.password_hash,
            )

            if not is_valid:
                raise InvalidCredentials("Invalid email or password.")

            payload: TokenPayload = {
                "user_id": user.id,
                "email": user.email,
            }

            token = self.token_provider.generate_access_token(payload)

            return AuthResult(
                access_token=token,
                user_id=user.id,
                email=user.email,
            )
        
    def get_user_from_token(self, token: str) -> User:
        try:
            payload: TokenPayload = self.token_provider.verify_token(token)
        except Exception:
            raise InvalidToken()

        with self.uow:
            user = self.uow.user_repo.get_by_id(payload["user_id"])

            if user is None:
                raise InvalidToken()

            return user