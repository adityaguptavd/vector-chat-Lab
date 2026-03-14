from app.application.interfaces.llm import AbstractLLM
from app.application.services.retrieval_service import RetrievalService
from app.infrastructure.vector.schemas.vector_document import VectorDocument
from typing import List

class RAGChatService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm: AbstractLLM,
    ) -> None:
        self._retrieval_service = retrieval_service
        self._llm = llm

    async def chat(self, user_id: str, query: str, top_k: int = 5) -> str:
        documents = self._retrieval_service.search(
            user_id=user_id,
            query=query,
            top_k=top_k,
        )

        context = self._build_context(documents)

        prompt = self._build_prompt(context=context, query=query)

        return await self._llm.generate(prompt)

    def _build_context(self, documents: List[VectorDocument]) -> str:
        return "\n\n".join(doc.content for doc in documents)

    def _build_prompt(self, context: str, query: str) -> str:
        return (
            "You are a helpful assistant.\n"
            "Use the context below to answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{query}\n\n"
            "Answer:"
        )