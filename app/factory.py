# factory.py

from fastapi import FastAPI
from .core.logging.logger import LoggingManager
from .core.logging.middleware import RequestLoggingMiddleware
from .core.handlers import register_exception_handlers
from .api.routers import users, auth, documents, chat
from app.infrastructure.db.init_db import init_db


def create_app():

    LoggingManager.configure()

    app = FastAPI()

    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)

    # Initiate DB
    init_db()

    app.include_router(users.router)
    app.include_router(auth.router)
    app.include_router(documents.router)
    app.include_router(chat.router)

    return app
