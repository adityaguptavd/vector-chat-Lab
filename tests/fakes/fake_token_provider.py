from app.domain.security.token_provider import (
    AbstractTokenProvider,
    TokenPayload,
)


class FakeTokenProvider(AbstractTokenProvider):

    def generate_access_token(self, payload: TokenPayload) -> str:
        return f"fake-token-for-{payload['user_id']}"

    def verify_token(self, token: str) -> TokenPayload:
        user_id = token.replace("fake-token-for-", "")
        return {
            "user_id": user_id,
            "email": "fake@example.com",
        }