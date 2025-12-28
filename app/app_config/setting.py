from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    PROD_DATABASE_URL:str
    TEST_DATABASE_URL:str
    TALLY_URL:str

    model_config = SettingsConfigDict(
        env_file = BASE_DIR/".env",
        env_file_encoding = "utf-8",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
