from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class FoodVendorData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True)

    name: str
    menu_url: str
    available_dates: list[date]
