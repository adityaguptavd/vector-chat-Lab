from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .exceptions import AppException
from app.domain.exceptions import DomainException, InvalidCredentials, InvalidToken, UserAlreadyExists, NotFoundError, ForbiddenError

from .logging.logger import LoggingManager
from .logging.context import request_id_ctx


logger = LoggingManager.get_logger("exceptions")


# ---------------- RESPONSE BUILDER ---------------- #

def build_error_response(status_code: int, message: str, errors=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "errors": errors,
            "request_id": request_id_ctx.get(),
        },
    )


# ---------------- REGISTER HANDLERS ---------------- #

def register_exception_handlers(app):

    # ---------- APP EXCEPTION ---------- #
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):

        logger.error(
            "APP_EXCEPTION",
            extra={"internal_message": exc.internal_message},
            exc_info=True,
        )

        return build_error_response(exc.status_code, exc.client_message)


    # ---------- DOMAIN BASE HANDLER ---------- #
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):

        logger.warning(
            "DOMAIN_EXCEPTION",
            extra={"error_message": exc.message},
        )

        return build_error_response(400, exc.message)


    # ---------- AUTH OVERRIDES ---------- #
    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentials):

        logger.warning("INVALID_CREDENTIALS")

        return build_error_response(401, exc.message)


    @app.exception_handler(InvalidToken)
    async def invalid_token_handler(request: Request, exc: InvalidToken):

        logger.warning("INVALID_TOKEN")

        return build_error_response(401, exc.message)


    # ---------- USER OVERRIDE ---------- #
    @app.exception_handler(UserAlreadyExists)
    async def user_exists_handler(request: Request, exc: UserAlreadyExists):

        logger.warning("USER_ALREADY_EXISTS")

        return build_error_response(409, exc.message)
    
    # ---------- ACCESS / RESOURCE OVERRIDES ---------- #

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):

        logger.warning("NOT_FOUND", extra={"error_message": exc.message})

        return build_error_response(404, exc.message)


    @app.exception_handler(ForbiddenError)
    async def forbidden_handler(request: Request, exc: ForbiddenError):

        logger.warning("FORBIDDEN", extra={"error_message": exc.message})

        return build_error_response(403, exc.message)


    # ---------- VALIDATION ---------- #
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):

        logger.warning("VALIDATION_ERROR", exc_info=True)

        return build_error_response(
            422,
            "Invalid request payload",
            errors=exc.errors(),
        )


    # ---------- FALLBACK ---------- #
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):

        logger.critical("UNHANDLED_EXCEPTION", exc_info=True)

        return build_error_response(500, "Internal server error")