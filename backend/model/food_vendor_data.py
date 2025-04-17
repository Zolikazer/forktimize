from datetime import date

from pydantic import BaseModel


class FoodVendorData(BaseModel):
    name: str
    menu_url: str
    available_dates: list[date]
