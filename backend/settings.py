import os
from pathlib import Path

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    ROOT_DIR: str = str(Path(__file__).parent.resolve())
    DATA_DIR: str = f"{ROOT_DIR}/resources"
    CITY_FOOD_API_URL: str = "https://ca.cityfood.hu"
    CITY_FOOD_API_FOOD_PATH: str = "api/v1/menu"
    DATABASE_PATH: str = f"/var/lib/forktimize/forktimize.db"
    DATABASE_CONNECTION_STRING: str = f"sqlite:///{DATABASE_PATH}"
    LOG_DIR: str = f"/var/log/forktimize"
    API_LOG_FILE: str = "api.log"
    JOB_LOG_FILE: str = "job.log"
    APP_LOG_FILE: str = "app.log"


class DevSettings(Settings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_PATH: str = f"{self.ROOT_DIR}/foods.db"
        self.DATABASE_CONNECTION_STRING: str = f"sqlite:///{self.DATABASE_PATH}"
        self.LOG_DIR: str = f"{self.ROOT_DIR}/logs/"


def get_settings() -> Settings:
    env = os.getenv("ENV", "development")
    return DevSettings() if env == "development" else Settings()


SETTINGS = get_settings()
