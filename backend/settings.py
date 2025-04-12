import os
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_ROOT_DIR: Path = Path(__file__).parent.resolve()
    FETCHING_DELAY: float = 0.5
    FETCHING_TIMEOUT: int = 30
    WEEKS_TO_FETCH: int = 3
    FETCH_IMAGES: bool = True

    CITY_FOOD_API_BASE: str = "https://ca.cityfood.hu"
    CITY_FOOD_IMAGE_URL_TEMPLATE: str = "https://ca.cityfood.hu/api/v1/i?menu_item_id={food_id}&width=425&height=425"

    INTER_FOOD_API_BASE: str = "https://ia.interfood.hu"
    INTER_FOOD_IMAGE_URL_TEMPLATE: str = "https://ia.interfood.hu/api/v1/i?menu_item_id={food_id}&width=425&height=425"

    INTER_CITY_FOOD_MENU_API_PATH: str = "api/v1/menu"

    TELETAL_MENU_URL: str = "https://www.teletal.hu/etlap"
    TELETAL_AJAX_URL: str = "https://www.teletal.hu/ajax"

    @computed_field
    def city_food_menu_url(self) -> str:
        return f"{self.CITY_FOOD_API_BASE}/{self.INTER_CITY_FOOD_MENU_API_PATH}"

    @computed_field
    def inter_food_menu_url(self) -> str:
        return f"{self.INTER_FOOD_API_BASE}/{self.INTER_CITY_FOOD_MENU_API_PATH}"

    LOG_DIR: str = "/var/log/forktimize"
    API_LOG_FILE: str = "api.log"
    JOB_LOG_FILE: str = "job.log"
    APP_LOG_FILE: str = "app.log"
    PERF_LOG_FILE: str = "perf.log"

    DATABASE_PATH: str = f"/var/lib/forktimize/forktimize.db"

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

    @computed_field
    @property
    def food_image_dir(self) -> Path:
        return self.PROJECT_ROOT_DIR / "images"


def get_settings() -> Settings:
    env = os.getenv("ENV", "development")
    return DevSettings() if env == "development" else Settings()


SETTINGS = get_settings()
