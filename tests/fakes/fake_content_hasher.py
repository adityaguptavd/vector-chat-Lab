from app.domain.services.content_hasher import AbstractContentHasher


class FakeContentHasher(AbstractContentHasher):

    def __init__(self) -> None:
        self.calls = []

    def hash(self, content: bytes) -> str:
        self.calls.append(content)
        return f"fake-hash-{content.decode()}"