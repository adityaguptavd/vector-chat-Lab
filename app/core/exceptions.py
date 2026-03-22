class AppException(Exception):

    def __init__(
        self,
        client_message: str,
        internal_message: str,
        status_code: int = 400,
        error_code: str | None = None,
        metadata: dict | None = None,
    ):
        super().__init__(internal_message)

        self.client_message = client_message
        self.internal_message = internal_message
        self.status_code = status_code
        self.error_code = error_code
        self.metadata = metadata or {}

class LLMServiceError(AppException):
    """Raised when LLM call fails"""

    def __init__(self, internal_message: str = "LLM service failure"):
        super().__init__(
            client_message="I'm having trouble generating a response. Please try again.",
            internal_message=internal_message,
            status_code=503,
            error_code="LLM_SERVICE_ERROR",
        )


class LLMTimeoutError(AppException):
    """Raised when LLM times out"""

    def __init__(self, internal_message: str = "LLM request timed out"):
        super().__init__(
            client_message="The request took too long. Please try again.",
            internal_message=internal_message,
            status_code=504,
            error_code="LLM_TIMEOUT",
        )


class LLMValidationError(AppException):
    """Raised when LLM response is invalid"""

    def __init__(self, internal_message: str = "Invalid LLM response"):
        super().__init__(
            client_message="Received an invalid response. Please retry.",
            internal_message=internal_message,
            status_code=502,
            error_code="LLM_VALIDATION_ERROR",
        )