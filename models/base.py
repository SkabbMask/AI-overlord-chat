from abc import ABC, abstractmethod


class ModelProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str, size: str) -> str:
        # size is "small" or "large"
        ...
