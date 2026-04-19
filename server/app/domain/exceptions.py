class DomainException(Exception):
    """Base class for all domain-level errors."""

    def __init__(self, message: str = "Domain error") -> None:
        self.message = message
        super().__init__(message)


# ---------------- AUTH ---------------- #

class AuthException(DomainException):
    """Base class for authentication-related domain errors."""
    pass


class InvalidCredentials(AuthException):
    def __init__(self, message: str = "Invalid email or password") -> None:
        super().__init__(message)


class InvalidToken(AuthException):
    def __init__(self, message: str = "Invalid or expired token") -> None:
        super().__init__(message)


# ---------------- USER ---------------- #

class UserAlreadyExists(DomainException):
    def __init__(self, message: str = "User already exists") -> None:
        super().__init__(message)

class NotFoundError(DomainException):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message)


class ForbiddenError(DomainException):
    def __init__(self, message: str = "Unauthorized access") -> None:
        super().__init__(message)

class UnsupportedFileType(DomainException):
    def __init__(self, message: str = "Unsupported file type") -> None:
        super().__init__(message)

class BadRequestError(DomainException):
    def __init__(self, message: str = "Bad Request") -> None:
        super().__init__(message)