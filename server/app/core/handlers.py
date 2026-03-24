from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.responses import ResponseBuilder

from .exceptions import AppException
from app.domain.exceptions import (
    DomainException, 
    InvalidCredentials, 
    InvalidToken, 
    UserAlreadyExists, 
    NotFoundError, 
    ForbiddenError,
    UnsupportedFileType
)

from .logging.logger import LoggingManager
from .logging.context import request_id_ctx


logger = LoggingManager.get_logger("exceptions")


# ---------------- REGISTER HANDLERS ---------------- #

def register_exception_handlers(app):

    # ---------- APP EXCEPTION ---------- #
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):

        logger.error(
            "APP_EXCEPTION",
            extra={
                "internal_message": exc.internal_message,
                "error_code": exc.error_code,
                "metadata": exc.metadata,
            },
            exc_info=True,
        )

        return ResponseBuilder.error(
            exc.status_code,
            exc.client_message,
            error_code=exc.error_code,
            metadata=exc.metadata,
        )


    # ---------- DOMAIN BASE HANDLER ---------- #
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):

        logger.warning(
            "DOMAIN_EXCEPTION",
            extra={"error_message": exc.message},
        )

        return ResponseBuilder.error(400, exc.message)


    # ---------- AUTH OVERRIDES ---------- #
    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentials):

        logger.warning("INVALID_CREDENTIALS")

        return ResponseBuilder.error(401, exc.message)


    @app.exception_handler(InvalidToken)
    async def invalid_token_handler(request: Request, exc: InvalidToken):

        logger.warning("INVALID_TOKEN")

        return ResponseBuilder.error(401, exc.message)


    # ---------- USER OVERRIDE ---------- #
    @app.exception_handler(UserAlreadyExists)
    async def user_exists_handler(request: Request, exc: UserAlreadyExists):

        logger.warning("USER_ALREADY_EXISTS")

        return ResponseBuilder.error(409, exc.message)
    
    # ---------- ACCESS / RESOURCE OVERRIDES ---------- #

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):

        logger.warning("NOT_FOUND", extra={"error_message": exc.message})

        return ResponseBuilder.error(404, exc.message)


    @app.exception_handler(ForbiddenError)
    async def forbidden_handler(request: Request, exc: ForbiddenError):

        logger.warning("FORBIDDEN", extra={"error_message": exc.message})

        return ResponseBuilder.error(403, exc.message)


    # ---------- VALIDATION ---------- #
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):

        logger.warning("VALIDATION_ERROR", exc_info=True)

        return ResponseBuilder.error(
            422,
            "Invalid request payload",
            errors=exc.errors(),
        )
    

    @app.exception_handler(UnsupportedFileType)
    async def unsupported_file_type_handler(request: Request, exc: UnsupportedFileType):

        logger.warning("UNSUPPORTED_FILE_TYPE")

        return ResponseBuilder.error(422, exc.message)


    # ---------- FALLBACK ---------- #
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):

        logger.critical("UNHANDLED_EXCEPTION", exc_info=True)

        return ResponseBuilder.error(500, "Internal server error")