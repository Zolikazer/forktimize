import os
from enum import Enum
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings

from constants import ONE_DAY


class RunMode(str, Enum):
    PRODUCTION = "production"
    TESTING = "testing"
    DEVELOPMENT = "development"


class Settings(BaseSettings):
    PROJECT_ROOT_DIR: Path = Path(__file__).parent.resolve()
    MODE: RunMode = RunMode.PRODUCTION
    FETCHING_DELAY: float = 0.5
    FETCHING_TIMEOUT: int = 30
    WEEKS_TO_FETCH: int = 3
    FETCH_IMAGES: bool = True
    INCLUDE_HEAVY_JOBS: bool = True
    HEADERS: dict[str, str] = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36"}

    # Cache settings
    DEFAULT_CACHE_SIZE: int = 50
    LARGE_CACHE_SIZE: int = 100
    DEFAULT_CACHE_TTL: int = 7 * ONE_DAY
    SHORT_CACHE_TTL: int = ONE_DAY

    CITY_FOOD_ORDERING_URL: str = "https://rendel.cityfood.hu/"
    CITY_FOOD_API_BASE: str = "https://ca.cityfood.hu"
    CITY_FOOD_IMAGE_URL_TEMPLATE: str = "https://ca.cityfood.hu/api/v1/i?menu_item_id={food_id}&width=425&height=425"

    INTER_FOOD_ORDERING_URL: str = "https://rendel.interfood.hu/"
    INTER_FOOD_API_BASE: str = "https://ia.interfood.hu"
    INTER_FOOD_IMAGE_URL_TEMPLATE: str = "https://ia.interfood.hu/api/v1/i?menu_item_id={food_id}&width=425&height=425"

    EFOOD_FOOD_ORDERING_URL: str = "https://rendel.e-food.hu/"
    EFOOD_FOOD_API_BASE: str = "https://ea.e-food.hu"
    EFOOD_FOOD_IMAGE_URL_TEMPLATE: str = "https://ea.e-food.hu/api/v1/i?menu_item_id={food_id}&width=425&height=425"

    INTER_CITY_FOOD_MENU_API_PATH: str = "api/v1/menu"

    TELETAL_MENU_URL: str = "https://www.teletal.hu/etlap"
    TELETAL_URL: str = "https://www.teletal.hu"

    @computed_field
    def teletal_menu_url(self) -> str:
        return f"{self.TELETAL_URL}/etlap"

    @computed_field
    def teletal_ajax_url(self) -> str:
        return f"{self.TELETAL_URL}/ajax"

    @computed_field
    def city_food_menu_api_url(self) -> str:
        return f"{self.CITY_FOOD_API_BASE}/{self.INTER_CITY_FOOD_MENU_API_PATH}"

    @computed_field
    def inter_food_menu_api_url(self) -> str:
        return f"{self.INTER_FOOD_API_BASE}/{self.INTER_CITY_FOOD_MENU_API_PATH}"

    @computed_field
    def efood_food_menu_api_url(self) -> str:
        return f"{self.EFOOD_FOOD_API_BASE}/{self.INTER_CITY_FOOD_MENU_API_PATH}"

    LOG_DIR: str = "/var/log/forktimize"
    API_LOG_FILE: str = "api.log"
    JOB_LOG_FILE: str = "job.log"
    APP_LOG_FILE: str = "app.log"
    PERF_LOG_FILE: str = "perf.log"

    DATABASE_PATH: str = f"/var/lib/forktimize/forktimize.db"
    DATABASE_BACKUP_ENABLED: bool = True
    DATABASE_BACKUP_BUCKET_NAME: str = "forktimize_backup"
    DATABASE_BACKUP_FILE_PREFIX: str = "forktimize-backup"
    DATABASE_BACKUP_INTERVAL_DAYS: int = 7
    DATABASE_BACKUP_LOCAL_FORMAT: str = "{stem}_backup_{timestamp}{suffix}"

    @computed_field
    def database_connection_string(self) -> str:
        return f"sqlite:///{self.DATABASE_PATH}"

    @computed_field
    def data_dir(self) -> Path:
        return self.PROJECT_ROOT_DIR / "resources"

    @computed_field
    def food_image_dir(self) -> Path:
        return Path("/var/www/forktimize/images")

    model_config = {
        "env_file": f"{PROJECT_ROOT_DIR}/.env",
        "env_file_encoding": "utf-8",
    }


class DevSettings(Settings):
    DATABASE_PATH: str = f"{Settings().PROJECT_ROOT_DIR}/forktimize.db"
    LOG_DIR: str = f"{Settings().PROJECT_ROOT_DIR}/logs"
    DATABASE_BACKUP_ENABLED: bool = False

    @computed_field
    def food_image_dir(self) -> Path:
        return self.PROJECT_ROOT_DIR / "images"


def get_settings() -> Settings:
    env = os.getenv("ENV", "development")
    return DevSettings() if env == "development" else Settings()


SETTINGS = get_settings()
