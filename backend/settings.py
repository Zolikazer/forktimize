from pathlib import Path

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATA_DIR: str = "resources"
    CITY_FOOD_API_URL: str = "https://ca.cityfood.hu"
    CITY_FOOD_API_FOOD_PATH: str = "api/v1/menu"
    ROOT_DIR: Path = Path(__file__).parent.resolve()
    DATABASE_PATH: Path = ROOT_DIR / "foods.db"
    DATABASE_LOCATION: str = f"sqlite:///{DATABASE_PATH}"


SETTINGS = Settings()
