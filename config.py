import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # ──────────────────────────────
    # 🗄️ DATABASE CONFIGURATION
    # ──────────────────────────────

    DB_PROTOCOL = os.getenv("DATABASE_PROTOCOL", "sqlite")
    DB_USER = os.getenv("DATABASE_USER", "")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_HOST = os.getenv("DATABASE_HOSTNAME", "")
    DB_PORT = os.getenv("DATABASE_PORT", "")
    DB_NAME = os.getenv("DATABASE_NAME", "url_shortner.db")

    if DB_PROTOCOL.lower() == "sqlite":
        # SQLite connection format: no username/password/host needed
        DATABASE_URL = f"sqlite:///{DB_NAME}"
    else:
        # Escape special characters in password
        encoded_password = quote_plus(DB_PASSWORD)
        DATABASE_URL = (
            f"{DB_PROTOCOL}://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    # ──────────────────────────────
    # 🔐 JWT CONFIGURATION
    # ──────────────────────────────

    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_insecure_dev_key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # ──────────────────────────────
    # 🔗 URL SHORTENER SETTINGS
    # ──────────────────────────────

    SHORT_URL_LENGTH = 8
    VERSION = "1.0.0"
    URL_PREFIX = os.getenv("URL_PREFIX", "/api")

    # ──────────────────────────────
    # 🧪 TEST DATA (Optional)
    # ──────────────────────────────

    TEST_USER = {
        "email": os.getenv("TEST_USER_EMAIL", "test@example.com"),
        "password": os.getenv("TEST_USER_PASSWORD", "password123"),
        "username": os.getenv("TEST_USER_USERNAME", "test_user")
    }

    AUTH_PAYLOAD = {
        "grant_type": "password",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
