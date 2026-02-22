# factory.py

from fastapi import FastAPI
from .core.logging.logger import LoggingManager
from .core.logging.middleware import RequestLoggingMiddleware
from .core.handlers import register_exception_handlers
from .routes.health import router as health_router


def create_app():

    LoggingManager.configure()

    app = FastAPI()

    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)

    app.include_router(health_router)

    return app
