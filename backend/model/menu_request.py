from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from datetime import date as date_type

from model.nutritional_constraints import NutritionalConstraints


class MenuRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True)

    date: date_type
    nutritional_constraints: NutritionalConstraints
    food_blacklist: list[str] = []
