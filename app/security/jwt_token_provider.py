import jwt
from datetime import datetime, timedelta, timezone
from typing import Any

from app.domain.security.token_provider import (
    AbstractTokenProvider,
    TokenPayload,
)


class JwtTokenProvider(AbstractTokenProvider):

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expires_minutes: int = 30,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expires_minutes = expires_minutes

    def generate_access_token(self, payload: TokenPayload) -> str:
        to_encode: dict[str, Any] = {
            "user_id": payload["user_id"],
            "email": payload["email"],
        }
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self._expires_minutes
        )
        to_encode["exp"] = expire

        return jwt.encode(
            to_encode,
            self._secret_key,
            algorithm=self._algorithm,
        )

    def verify_token(self, token: str) -> TokenPayload:
        decoded = jwt.decode(
            token,
            self._secret_key,
            algorithms=[self._algorithm],
        )

        return {
            "user_id": decoded["user_id"],
            "email": decoded["email"],
        }