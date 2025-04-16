from datetime import date

from pydantic import BaseModel


class FoodProviderData(BaseModel):
    name: str
    available_dates: list[date]
    url: str