import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import *
from models.size_selector import select_size
from prompt_builder import *
from storage.local import LocalStorage
from storage.convex import ConvexStorage
from models.claude import ClaudeProvider
from models.gemini import GeminiProvider

logger = logging.getLogger(__name__)
app = FastAPI()


class ChatRequest(BaseModel):
    question_id: str
    user_message: str
    model_family: Optional[str] = None


def _get_storage():
    backend = STORAGE_BACKEND
    if backend == "convex":
        if not CONVEX_URL:
            raise RuntimeError("CONVEX_URL must be set when STORAGE_BACKEND=convex")
        return ConvexStorage(convex_url=CONVEX_URL)
    return LocalStorage()


def _get_provider(model_family: str):
    if model_family == "gemini":
        return GeminiProvider(api_key=GEMINI_API_KEY)
    return ClaudeProvider(api_key=ANTHROPIC_API_KEY)


@app.post("/chat")
def chat(request: ChatRequest):
    storage = _get_storage()
    model_family = request.model_family or MODEL_FAMILY
    provider = _get_provider(model_family)

    try:
        strategy = storage.get_strategy(request.question_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    small_provider = _get_provider(model_family)

    user_question = request.user_message
    question_verification_prompt = build_user_question_verification_prompt(user_question, strategy)
    question_verification = small_provider.complete(question_verification_prompt, "small")
    if question_verification.startswith("FAIL"):
        logger.warning("User question verification failed%s", user_question)
        raise HTTPException(status_code=400)
    
    model_size = select_size({"strategy": strategy})
    prompt = build_prompt(user_question, strategy)
    answer = provider.complete(prompt, model_size)

    verification_prompt = build_model_answer_verification_prompt(answer, strategy)
    verification = small_provider.complete(verification_prompt, "small")

    retries = 0
    while retries < VERIFICATION_FAILED_RETRIES and verification.startswith("FAIL"):
        logger.warning("Verification FAILED for question_id=%s: %s", request.question_id, verification)
        prompt = build_retry_prompt(user_question, strategy, answer)
        answer = provider.complete(prompt, model_size)
        verification_prompt = build_model_answer_verification_prompt(answer, strategy)
        verification = small_provider.complete(verification_prompt, "small")
        retries += 1
    
    if verification.startswith("FAIL"):
        logger.warning("Verification failed after %s tries, model answer '%s' not accepted", retries, answer)
        raise HTTPException(status_code=400)

    return {"answer": answer}
