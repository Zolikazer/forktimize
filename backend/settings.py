from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATA_DIR: str = "resources"


settings = Settings()
