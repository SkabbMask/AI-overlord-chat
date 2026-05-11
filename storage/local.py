import json
import os
from .base import StorageBase

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "strategies.json")


class LocalStorage(StorageBase):
    def get_strategy(self, question_id: str) -> str:
        with open(_DATA_PATH, "r") as f:
            data = json.load(f)
        if question_id not in data:
            raise KeyError(f"Question ID '{question_id}' not found in local storage")
        return data[question_id]["strategy"]
