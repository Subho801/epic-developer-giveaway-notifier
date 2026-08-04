import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()

COUNTRY = os.getenv("COUNTRY", "US").upper()

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))

ROLE_ID = os.getenv("ROLE_ID", "").strip()


def validate():
    """Validate required configuration."""

    if not WEBHOOK_URL:
        raise ValueError("WEBHOOK_URL is missing in .env")

    if CHECK_INTERVAL < 30:
        raise ValueError("CHECK_INTERVAL must be at least 30 seconds")
