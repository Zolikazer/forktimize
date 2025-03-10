from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATA_DIR: str = "resources"
    CITY_FOOD_API_URL: str = "https://ca.cityfood.hu"
    CITY_FOOD_API_FOOD_PATH = "api/v1/menu"


SETTINGS = Settings()
