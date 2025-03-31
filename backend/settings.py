import os
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_ROOT_DIR: Path = Path(__file__).parent.resolve()

    CITY_FOOD_API_BASE: str = "https://ca.cityfood.hu"
    INTER_FOOD_API_BASE: str = "https://ia.interfood.hu"
    INTER_CITY_FOOD_MENU_API_PATH: str = "api/v1/menu"

    @computed_field
    @property
    def CITY_FOOD_MENU_URL(self) -> str:
        return f"{self.CITY_FOOD_API_BASE}/{self.INTER_CITY_FOOD_MENU_API_PATH}"

    @computed_field
    @property
    def INTER_FOOD_MENU_URL(self) -> str:
        return f"{self.INTER_FOOD_API_BASE}/{self.INTER_CITY_FOOD_MENU_API_PATH}"

    LOG_DIR: str = "/var/log/forktimize"
    ENABLE_LOG_FLUSH: bool = False
    API_LOG_FILE: str = "api.log"
    JOB_LOG_FILE: str = "job.log"
    APP_LOG_FILE: str = "app.log"
    PERF_LOG_FILE: str = "perf.log"

    DATABASE_PATH: str = f"/var/lib/forktimize/forktimize.db"

    @computed_field
    @property
    def DATABASE_CONNECTION_STRING(self) -> str:
        return f"sqlite:///{self.DATABASE_PATH}"

    @computed_field
    @property
    def DATA_DIR(self) -> Path:
        return self.PROJECT_ROOT_DIR / "resources"

    model_config = {
        "env_file": f"{PROJECT_ROOT_DIR}/.env",
        "env_file_encoding": "utf-8",
    }


class DevSettings(Settings):
    DATABASE_PATH: str = f"{Settings().PROJECT_ROOT_DIR}/forktimize.db"
    LOG_DIR: str = f"{Settings().PROJECT_ROOT_DIR}/logs"


def get_settings() -> Settings:
    env = os.getenv("ENV", "development")
    return DevSettings() if env == "development" else Settings()


SETTINGS = get_settings()
