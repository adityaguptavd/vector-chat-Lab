from app.application.services.chat_service import ChatService
from app.application.services.user_service import UserService
from app.application.services.document_service import DocumentService
from app.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.security.bcrypt_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_token_provider import JwtTokenProvider
from app.infrastructure.security.sha_256_hasher import Sha256ContentHasher
from app.application.services.document_ingestor import SimpleDocumentIngestor
from app.application.services.retrieval_service import RetrievalService
from tests.fakes.fake_llm import FakeLLM
from app.infrastructure.vector.faiss_user_vector_store_manager import FAISSUserVectorStoreManager
# from app.infrastructure.vector.local_embedder import LocalSentenceTransformerEmbedder
from tests.fakes.fake_embedder import FakeEmbedder
from tests.fakes.fake_user_vector_store_manager import FakeUserVectorStoreManager
from app.application.services.chunker import SimpleChunker


def test_chat_service_returns_llm_response(db_session):
    uow = SqlAlchemyUnitOfWork(db_session)
    user_service = UserService(
        uow=uow,
        password_hasher=BcryptPasswordHasher(),
        token_provider=JwtTokenProvider(secret_key="SECRET_KEY"),
    )

    user_vector_manager = FakeUserVectorStoreManager()

    document_service = DocumentService(
        uow=uow,
        ingestor=SimpleDocumentIngestor(
            user_vector_manager=user_vector_manager, 
            embedder=FakeEmbedder(), 
            chunker=SimpleChunker()
            ),
        content_hasher=Sha256ContentHasher()
    )

    retrieval_service = RetrievalService(
        user_vector_manager=user_vector_manager,
        embedder=FakeEmbedder()
    )

    user = user_service.register_user(
        email="email@example.com",
        raw_password="password123",
    )

    document_service.upload_document(
        user_id=user.id,
        filename="document.txt",
        content=b"Python is a programming language.",
    )

    fake_llm = FakeLLM()

    chat_service = ChatService(
        retrieval_service=retrieval_service,
        llm=fake_llm,
    )

    # Act
    response = chat_service.chat(
        user_id=user.id,
        query="What is Python?",
    )

    # Assert
    assert response == "fake-response"
    assert fake_llm.last_prompt is not None
    assert "Python is a programming language." in fake_llm.last_prompt
    assert "What is Python?" in fake_llm.last_prompt