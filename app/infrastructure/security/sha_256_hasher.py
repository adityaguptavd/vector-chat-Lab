import hashlib
from app.domain.core.content_hasher import AbstractContentHasher


class Sha256ContentHasher(AbstractContentHasher):

    def hash(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()