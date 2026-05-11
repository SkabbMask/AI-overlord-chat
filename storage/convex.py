import httpx
from .base import StorageBase


class ConvexStorage(StorageBase):
    def __init__(self, convex_url: str):
        self.convex_url = convex_url.rstrip("/")

    def get_strategy(self, question_id: str) -> str:
        url = f"{self.convex_url}/getStrategy"
        try:
            response = httpx.get(url, params={"questionId": question_id}, timeout=10.0)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise KeyError(f"Question ID '{question_id}' not found in Convex") from e
            raise RuntimeError(f"Convex request failed: {e}") from e
        except httpx.RequestError as e:
            raise RuntimeError(f"Convex request error: {e}") from e

        data = response.json()
        if "strategy" not in data:
            raise KeyError(f"Question ID '{question_id}' returned no strategy from Convex")
        return data["strategy"]
