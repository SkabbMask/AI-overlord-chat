from typing import Optional
from google import genai
from .base import ModelProvider

_MODEL_MAP = {
    "small": "gemini-2.5-pro",
    "large": "gemini-2.5-pro",
}


class GeminiProvider(ModelProvider):
    def __init__(self, api_key: Optional[str] = None):
        self._client = genai.Client(api_key=api_key)

    def complete(self, prompt: str, size: str) -> str:
        model_name = _MODEL_MAP.get(size, _MODEL_MAP["large"])
        response = self._client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
