
import os
from pathlib import Path
from dotenv import load_dotenv


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from root .env file
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)


# Application Configuration
APP_NAME = os.getenv(
    "APP_NAME",
    "IT Service Desk AI Agent"
)

APP_ENV = os.getenv("APP_ENV", "development")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./data/service_desk.db"
)


# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def validate_config():
    """Validate required application configuration."""

    errors = []

    if not GROQ_API_KEY:
        errors.append("GROQ_API_KEY is missing")

    if not GOOGLE_API_KEY:
        errors.append("GOOGLE_API_KEY is missing")

    if errors:
        raise ValueError(
            "Configuration Error: " + ", ".join(errors)
        )

    return True
