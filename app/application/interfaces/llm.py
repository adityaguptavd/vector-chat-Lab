from typing import Protocol

class AbstractLLM(Protocol):
    def generate(self, prompt: str) -> str:
        pass