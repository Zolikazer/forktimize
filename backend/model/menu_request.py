from typing import List

from pydantic import BaseModel, ConfigDict

from model.alias_generator import to_camel
from model.nutritional_constraints import NutritionalConstraints


class MenuRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True)

    date: str
    nutritional_constraints: NutritionalConstraints
    food_blacklist: List[str] = []

