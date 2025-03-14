from pathlib import Path

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATA_DIR: str = "resources"
    CITY_FOOD_API_URL: str = "https://ca.cityfood.hu"
    CITY_FOOD_API_FOOD_PATH: str = "api/v1/menu"
    ROOT_DIR: Path = Path(__file__).parent.resolve()  # 🔥 Get root directory
    DATABASE_PATH: Path = ROOT_DIR / "foods.db"  # 🔥 Store DB in root directory
    DATABASE_LOCATION: str = f"sqlite:///{DATABASE_PATH}"
    TEST_MODE: bool = False


SETTINGS = Settings()
