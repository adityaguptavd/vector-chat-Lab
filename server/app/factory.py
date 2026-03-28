# factory.py

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from .core.logging.logger import LoggingManager
from .core.logging.middleware import RequestLoggingMiddleware
from .core.handlers import register_exception_handlers
from .api.routers import users, auth, documents, chat
from app.infrastructure.db.init_db import init_db
from fastapi.middleware.cors import CORSMiddleware


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="VectorChat-Lab",
        version="0.1.0",
        description="API docs",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_app():

    LoggingManager.configure()

    app = FastAPI()
    app.openapi = lambda: custom_openapi(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # your frontend
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)

    # Initiate DB
    init_db()

    app.include_router(users.router)
    app.include_router(auth.router)
    app.include_router(documents.router)
    app.include_router(chat.router)

    return app
