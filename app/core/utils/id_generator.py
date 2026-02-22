import uuid
import secrets
from datetime import datetime, timezone


class IDGenerator:

    @staticmethod
    def generate(
        prefix: str | None = None,
        length: int = 12,
        time_sortable: bool = False
    ) -> str:
        if time_sortable:
            time_part = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
            random_part = secrets.token_urlsafe(length)[:length]
            base = f"{time_part}_{random_part}"
        else:
            base = secrets.token_urlsafe(length)[:length]

        return f"{prefix}_{base}" if prefix else base
