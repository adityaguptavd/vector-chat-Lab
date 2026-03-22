from app.application.interfaces.llm import AbstractLLM
from app.application.services.retrieval_service import RetrievalService
from app.infrastructure.vector.schemas.vector_document import VectorDocument
from app.core.utils.llm_validator import LLMResponseValidator
from typing import List, AsyncGenerator

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

        if not documents:
            return "I'm sorry but I couldn't find any relevant information in the provided documents."

        context = self._build_context(documents)

        messages = self._build_messages(context=context, query=query)

        response = await self._llm.generate(messages)

        validated = LLMResponseValidator.validate(response)
        return validated
    
    async def stream_chat(self, user_id: str, query: str, top_k: int = 5) -> AsyncGenerator[str, None]:
        documents = self._retrieval_service.search(
            user_id=user_id,
            query=query,
            top_k=top_k,
        )

        if not documents:
            yield "I'm sorry but I couldn't find any relevant information in the provided documents."
            return

        context = self._build_context(documents)

        messages = self._build_messages(context=context, query=query)

        async for chunk in self._llm.stream(messages):
            yield chunk

    def _build_context(self, documents: List[VectorDocument]) -> str:
        return "\n\n".join(doc.content for doc in documents)

    def _build_messages(self, context: str, query: str) -> list[dict]:
        return [
            {
                "role": "system",
                "content": """
You are a strict AI assistant.

RULES:
- Answer ONLY using the provided context
- Do NOT use external knowledge

Response style:
- Clear and direct
- No unnecessary explanations
""".strip(),
            },
            {
                "role": "user",
                "content": f"""
    Context:
    {context}

    Question:
    {query}
    """.strip(),
            },
        ]