import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent.parent

load_dotenv()


class Settings:
    config_url: str = os.getenv("CONFIG_URL")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"

    @classmethod
    def async_db_url(cls):
        return f"postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
