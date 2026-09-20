"""Configuration loaded from environment variables."""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    lm_studio_url: str
    bot_username: str | None
    knowledge_dir: Path
    index_dir: Path
    log_level: str

    @classmethod
    def from_environment(cls) -> "Settings":
        load_dotenv(PROJECT_ROOT / ".env")
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is missing. Copy .env.example to .env and add it.")
        username = os.getenv("BOT_USERNAME", "").strip().lstrip("@") or None
        return cls(
            telegram_bot_token=token,
            lm_studio_url=os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1"),
            bot_username=username,
            knowledge_dir=PROJECT_ROOT / "data",
            index_dir=PROJECT_ROOT / "storage" / "faiss",
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )
