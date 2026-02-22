class AppException(Exception):

    def __init__(
        self,
        client_message: str,
        internal_message: str,
        status_code: int = 400
    ):
        self.client_message = client_message
        self.internal_message = internal_message
        self.status_code = status_code