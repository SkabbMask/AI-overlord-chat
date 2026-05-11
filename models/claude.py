import anthropic
from typing import Optional
from .base import ModelProvider

_MODEL_MAP = {
    "small": "claude-haiku-4-5",
    "large": "claude-sonnet-4-6",
}


class ClaudeProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None):
        self._client = anthropic.Anthropic(api_key=api_key)

    def complete(self, prompt: str, size: str) -> str:
        model = _MODEL_MAP.get(size, _MODEL_MAP["large"])
        response = self._client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        for block in response.content:
            if block.type == "text":
                return block.text
        return ""
