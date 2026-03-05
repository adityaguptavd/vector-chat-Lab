class DomainException(Exception):
    """Base class for all domain-level errors."""

    def __init__(self, message: str = "Domain error"):
        self.message = message
        super().__init__(message)


# ---------------- AUTH ---------------- #

class AuthException(DomainException):
    """Base class for authentication-related domain errors."""
    pass


class InvalidCredentials(AuthException):
    def __init__(self):
        super().__init__("Invalid email or password")


class InvalidToken(AuthException):
    def __init__(self):
        super().__init__("Invalid or expired token")


# ---------------- USER ---------------- #

class UserAlreadyExists(DomainException):
    def __init__(self):
        super().__init__("User already exists")