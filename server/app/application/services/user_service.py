from app.domain.unit_of_work import AbstractUnitOfWork
from app.domain.security.password_hasher import AbstractPasswordHasher
from app.domain.security.token_provider import AbstractTokenProvider
from app.domain.user import User
from app.domain.exceptions import UserAlreadyExists, InvalidCredentials, InvalidToken
from app.domain.security.token_provider import TokenPayload
from app.application.dto.auth import AuthResult
from app.core.logging.logger import LoggingManager

logger = LoggingManager.get_logger("user_service")

class UserService:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        password_hasher: AbstractPasswordHasher,
        token_provider: AbstractTokenProvider,
    ) -> None:
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_provider = token_provider

    def register_user(self, email: str, raw_password: str, full_name: str) -> User:
        logger.debug("Registration attempt", extra={"event": "register_attempt", "email": email})

        with self.uow as uow:
            if uow.user_repo.exists_by_email(email):
                logger.warning("Registration failed", extra={"event": "register_failed", "email": email})
                raise UserAlreadyExists()

            hashed = self.password_hasher.hash(raw_password)

            user = User.create(email=email, password_hash=hashed, full_name=full_name)
            created = uow.user_repo.create(user)

            logger.info("Registration success", extra={"event": "register_success", "user_id": user.id})
            return created
        
    def login_user(self, email: str, raw_password: str) -> AuthResult:
        logger.debug("Login attempt", extra={"event": "login_attempt", "email": email})

        with self.uow as uow:
            user = uow.user_repo.get_by_email(email)

            if user is None or not self.password_hasher.verify(raw_password, user.password_hash):
                logger.warning("Login failed", extra={"event": "login_failed", "email": email})
                raise InvalidCredentials()

            payload: TokenPayload = {"user_id": user.id, "email": user.email}
            token = self.token_provider.generate_access_token(payload)

            logger.info("Login success", extra={"event": "login_success", "user_id": user.id})

            return AuthResult(access_token=token, user_id=user.id, email=user.email, full_name=user.full_name)
        
    def get_user_from_token(self, token: str) -> User:
        logger.debug("Token verification attempt", extra={"event": "token_verify_attempt"})

        try:
            payload = self.token_provider.verify_token(token)
        except Exception as e:
            logger.warning("Invalid token", extra={"event": "token_invalid"})
            raise InvalidToken() from e

        with self.uow as uow:
            user = uow.user_repo.get_by_id(payload["user_id"])

            if user is None:
                logger.warning("Token verification failed", extra={"event": "token_no_user"})
                raise InvalidToken()

            logger.info("Token verified", extra={"event": "token_verified", "user_id": user.id})
            return user