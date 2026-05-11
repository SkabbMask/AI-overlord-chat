from dotenv import load_dotenv
import os

load_dotenv()

MODEL_FAMILY = os.getenv("MODEL_FAMILY", "claude")
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")
CONVEX_URL = os.getenv("CONVEX_URL")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

VERIFICATION_FAILED_RETRIES = 2