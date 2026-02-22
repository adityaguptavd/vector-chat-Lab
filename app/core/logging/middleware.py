from time import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..utils.id_generator import IDGenerator
from .context import request_id_ctx
from .logger import LoggingManager


logger = LoggingManager.get_logger("middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = IDGenerator.generate(prefix="req", time_sortable=True)
        request_id_ctx.set(request_id)

        start_time = time()

        logger.info(f"REQUEST_STARTED {request.method} {request.url.path}")

        try:
            response = await call_next(request)
        except Exception:
            duration = int((time() - start_time) * 1000)
            logger.exception("UNHANDLED_EXCEPTION", extra={"duration_ms": duration})
            raise

        duration = int((time() - start_time) * 1000)

        logger.info(
            f"REQUEST_COMPLETED {request.method} {request.url.path}",
            extra={"duration_ms": duration}
        )

        response.headers["X-Request-ID"] = request_id
        return response
