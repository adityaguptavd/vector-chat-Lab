# core/handlers.py

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .exceptions import AppException
from .logging.logger import LoggingManager
from .logging.context import request_id_ctx

logger = LoggingManager.get_logger("exceptions")


def register_exception_handlers(app):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):

        logger.error(
            exc.internal_message,
            exc_info=True
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.client_message,
                "request_id": request_id_ctx.get()
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):

        logger.warning("Validation error", exc_info=True)

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Invalid request payload",
                "errors": exc.errors(),
                "request_id": request_id_ctx.get()
            }
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):

        logger.critical("Unhandled exception", exc_info=True)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error",
                "request_id": request_id_ctx.get()
            }
        )
