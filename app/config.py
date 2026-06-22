"""
Application configuration.

All secrets and tunable settings are loaded from environment variables
(via a local .env file in development). Never hardcode credentials here.
"""

import os
import sys
import logging

from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
#  🔑 SECRETS
# ─────────────────────────────────────────────

TELEGRAM_BOT_TOKEN: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")

# ─────────────────────────────────────────────
#  ⚙️ SETTINGS
# ─────────────────────────────────────────────

GROQ_API_URL: str = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
AI_MODEL: str = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")
MAX_MEMORY: int = int(os.getenv("MAX_MEMORY", "20"))
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "20"))

# ─────────────────────────────────────────────
#  📝 LOGGING
# ─────────────────────────────────────────────


def configure_logging() -> None:
    """Configure root logging format/level for the whole application."""
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
    )


def validate_config() -> None:
    """Fail fast with a clear error if required secrets are missing."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")

    if missing:
        logging.error(
            "Missing required environment variable(s): %s. "
            "Copy .env.example to .env and fill in the values.",
            ", ".join(missing),
        )
        sys.exit(1)
