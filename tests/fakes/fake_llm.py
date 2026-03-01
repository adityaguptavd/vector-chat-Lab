class FakeLLM:
    def __init__(self) -> None:
        self.last_prompt = None

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return "fake-response"