# Python Logic Service

A self-contained Python service that receives a user question, fetches an AI strategy from a storage backend, constructs a prompt, routes it to an LLM, and returns a text response.

## How to run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `MODEL_FAMILY` | `claude` | Which LLM provider to use: `claude` or `gemini` |
| `STORAGE_BACKEND` | `local` | Where to fetch strategies: `local` or `convex` |
| `CONVEX_URL` | — | Base URL of your Convex deployment (required when `STORAGE_BACKEND=convex`) |
| `ANTHROPIC_API_KEY` | — | API key for Claude models |
| `GEMINI_API_KEY` | — | API key for Gemini models |

Copy `.env.example` to `.env` and fill in the values, or export them in your shell.

## Switching storage backend

Set `STORAGE_BACKEND=convex` and provide `CONVEX_URL` to route strategy lookups to a Convex deployment instead of the local `data/strategies.json` file.

## Switching model family

Set `MODEL_FAMILY=gemini` to route completions through Gemini instead of Claude. The request body also accepts a `model_family` field to override the env var per request.

## Adding a new model provider

1. Create a new file in `models/` (e.g. `models/openai.py`).
2. Subclass `ModelProvider` from `models/base.py` and implement `complete(prompt, size) -> str`.
3. Add a branch in `main.py`'s `_get_provider()` factory for the new family name.

## Adding a new storage backend

1. Create a new file in `storage/` (e.g. `storage/redis.py`).
2. Subclass `StorageBase` from `storage/base.py` and implement `get_strategy(question_id) -> str`.
3. Add a branch in `main.py`'s `_get_storage()` factory for the new backend name.

## API

### `POST /chat`

Example:
```
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question_id": "question_1", "user_message": "Surely an AI would not actually do this?"}'
```

**Request body:**
```json
{
  "question_id": "question_1",
  "user_message": "But surely an AI wouldn't actually do this?",
  "model_family": "claude"
}
```

**Response:**
```json
{
  "answer": "..."
}
```
