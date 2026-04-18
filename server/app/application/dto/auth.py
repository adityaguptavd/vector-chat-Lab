from dataclasses import dataclass

@dataclass(frozen=True)
class AuthResult:
    access_token: str
    user_id: str
    email: str
    full_name: str | None