class DomainException(Exception):
    """Base class for domain-level errors."""
    pass


class InvalidCredentials(Exception):
    """Raised when authentication fails due to invalid email or password."""
    pass

class UserAlreadyExists(DomainException):
    pass

class InvalidToken(DomainException):
    pass