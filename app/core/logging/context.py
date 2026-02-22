from contextvars import ContextVar

request_id_ctx = ContextVar("request_id", default=None)
user_id_ctx = ContextVar("user_id", default=None)
