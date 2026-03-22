from app.core.exceptions import LLMValidationError

class LLMResponseValidator:

    MAX_LENGTH = 5000

    @classmethod
    def validate(cls, text: str) -> str:
        if text is None:
            raise LLMValidationError("LLM returned None")

        cleaned = text.strip()

        # 1️⃣ Empty response
        if not cleaned:
            raise LLMValidationError("Empty LLM response")

        # 2️⃣ Too long (safety guard)
        if len(cleaned) > cls.MAX_LENGTH:
            raise LLMValidationError("LLM response too long")

        # 3️⃣ Prompt leakage detection
        leakage_signals = [
            "You are an AI assistant",
            "Context:",
            "Question:",
            "SYSTEM_PROMPT",
        ]

        for signal in leakage_signals:
            if signal.lower() in cleaned.lower():
                raise LLMValidationError("Prompt leakage detected")

        return cleaned