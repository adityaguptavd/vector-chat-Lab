from abc import ABC, abstractmethod
from typing import TypedDict


class TokenPayload(TypedDict):
    user_id: str
    email: str


class AbstractTokenProvider(ABC):

    @abstractmethod
    def generate_access_token(self, payload: TokenPayload) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> TokenPayload:
        pass