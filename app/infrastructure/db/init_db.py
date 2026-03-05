from app.infrastructure.db.session import engine
from app.infrastructure.db.base import Base

# import models so SQLAlchemy registers them
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.models.document_model import DocumentModel


def init_db():
    Base.metadata.create_all(bind=engine)