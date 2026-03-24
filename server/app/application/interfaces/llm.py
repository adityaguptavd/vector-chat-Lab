from typing import Protocol, AsyncGenerator

class AbstractLLM(Protocol):
    def generate(self, messages: list[dict]) -> str:
        pass

    async def generate(self, messages: list[dict]) -> str:
        pass

    async def stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        pass