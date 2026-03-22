from groq import Groq
from app.application.interfaces.llm import AbstractLLM
from app.core.exceptions import LLMTimeoutError, LLMServiceError
import asyncio
from queue import Queue
from threading import Thread
from typing import AsyncGenerator

class GroqLLM(AbstractLLM):
    def __init__(self, api_key: str, model: str):
        self._client = Groq(api_key=api_key)
        self._model = model

    def generate_sync(self, messages: list[dict]) -> str:
        # Groq SDK is sync → run safely later if needed
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=0.0,
            )
            return response.choices[0].message.content
        except TimeoutError as e:
            raise LLMTimeoutError(str(e))
        except Exception as e:
            raise LLMServiceError(str(e))

    
    async def generate(self, messages: list[dict]) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate_sync, messages)
    
    async def stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:

        queue: Queue = Queue()
        loop = asyncio.get_event_loop()

        def worker():
            try:
                stream = self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    temperature=0.0,
                    stream=True,
                )

                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        queue.put(content)

            except Exception as e:
                queue.put(LLMServiceError(str(e)))

            finally:
                queue.put(None)

        Thread(target=worker, daemon=True).start()

        while True:
            item = await loop.run_in_executor(None, queue.get)

            if item is None:
                break

            if isinstance(item, Exception):
                raise item

            yield item