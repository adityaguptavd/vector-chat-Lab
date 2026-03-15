from typing import Generator
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.security.bcrypt_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_token_provider import JwtTokenProvider
from app.application.services.user_service import UserService
from app.application.services.document_service import DocumentService
from app.application.services.document_ingestor import SimpleDocumentIngestor
from app.infrastructure.security.sha_256_hasher import Sha256ContentHasher
from app.application.services.chunker import SimpleChunker
from app.application.services.chat_service import ChatService
from app.domain.unit_of_work import AbstractUnitOfWork
from app.domain.security.password_hasher import AbstractPasswordHasher
from app.domain.security.token_provider import AbstractTokenProvider
from app.domain.core.document_ingestor import AbstractDocumentIngestor
from app.domain.core.content_hasher import AbstractContentHasher
from app.application.interfaces.llm import AbstractLLM
from app.application.services.rag_chat_service import RAGChatService
from app.application.services.retrieval_service import RetrievalService
from app.infrastructure.vector.faiss_user_vector_store_manager import FAISSUserVectorStoreManager
from app.infrastructure.vector.local_embedder import LocalSentenceTransformerEmbedder
from tests.fakes.fake_llm import FakeLLM
from app.core.config import settings
from app.domain.exceptions import InvalidToken
from fastapi import Depends
from app.domain.user import User
from app.core.logging.context import user_id_ctx

# 🔥 SINGLETONS
_embedder = LocalSentenceTransformerEmbedder(model_name=settings.EMBEDDING_MODEL)

_vector_manager = FAISSUserVectorStoreManager(
    base_path="/app/vector_store",
    embedding_dim=_embedder.dimension,
)

def _get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_uow(db: Session = Depends(_get_db)) -> AbstractUnitOfWork:
    return SqlAlchemyUnitOfWork(db)


def get_password_hasher() -> AbstractPasswordHasher:
    return BcryptPasswordHasher()

def get_token_provider() -> AbstractTokenProvider:
    return JwtTokenProvider(secret_key=settings.JWT_SECRET)

def get_document_ingestor() -> AbstractDocumentIngestor:
    return SimpleDocumentIngestor(
        user_vector_manager=_vector_manager,
        embedder=_embedder,
        chunker=SimpleChunker()
    )

def get_content_hasher() -> AbstractContentHasher:
    return Sha256ContentHasher()

def get_bearer_token(authorization: str | None = Header(default=None, include_in_schema=False)) -> str:
    if not authorization:
        raise InvalidToken()

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise InvalidToken()

    return token

def get_retrieval_service() -> RetrievalService:

    return RetrievalService(
        user_vector_manager=_vector_manager,
        embedder=_embedder,
    )

def get_llm() -> AbstractLLM:
    return FakeLLM()  # later swap with OpenAI


def get_rag_chat_service(
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
    llm: AbstractLLM = Depends(get_llm),
) -> RAGChatService:

    return RAGChatService(
        retrieval_service=retrieval_service,
        llm=llm,
    )

def get_user_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    password_hasher: AbstractPasswordHasher = Depends(get_password_hasher),
    token_provider: AbstractTokenProvider = Depends(get_token_provider),
) -> UserService:

    return UserService(
        uow=uow,
        password_hasher=password_hasher,
        token_provider=token_provider,
    )

def get_document_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    document_ingestor: AbstractDocumentIngestor = Depends(get_document_ingestor),
    content_hasher: AbstractTokenProvider = Depends(get_content_hasher),
) -> DocumentService:

    return DocumentService(
        uow=uow,
        ingestor=document_ingestor,
        content_hasher=content_hasher
    )

async def get_current_user(
    token: str = Depends(get_bearer_token),
    user_service: UserService = Depends(get_user_service),
) -> User:

    user = user_service.get_user_from_token(token)

    # inject into logging context
    user_id_ctx.set(user.id)

    return user

def get_chat_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    rag_chat_service: RAGChatService = Depends(get_rag_chat_service),
) -> ChatService:

    return ChatService(
        uow=uow,
        rag_chat_service=rag_chat_service,
    )