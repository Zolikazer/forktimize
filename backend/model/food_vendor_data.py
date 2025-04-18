from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from food_vendors.food_vendor_type import FoodVendorType


class FoodVendorData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True)

    name: str
    type: FoodVendorType
    menu_url: str
    available_dates: list[date]
