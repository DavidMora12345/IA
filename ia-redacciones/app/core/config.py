import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    engine: str = os.getenv("ENGINE", "rules").lower()
    ollama_base_url: str | None = os.getenv("OLLAMA_BASE_URL")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

settings = Settings()
