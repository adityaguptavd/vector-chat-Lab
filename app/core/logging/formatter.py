import logging
import json
from datetime import datetime, timezone
from .context import request_id_ctx, user_id_ctx


class JSONFormatter(logging.Formatter):

    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "request_id": request_id_ctx.get(),
            "user_id": user_id_ctx.get(),
            "module": record.module,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)
