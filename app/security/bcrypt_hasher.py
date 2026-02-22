import bcrypt
from app.domain.security.password_hasher import AbstractPasswordHasher


class BcryptPasswordHasher(AbstractPasswordHasher):

    def hash(self, raw_password: str) -> str:
        return bcrypt.hashpw(
            raw_password.encode(),
            bcrypt.gensalt()
        ).decode()

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            raw_password.encode(),
            hashed_password.encode()
        )