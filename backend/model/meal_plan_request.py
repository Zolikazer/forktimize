from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveInt
from pydantic.alias_generators import to_camel
from datetime import date as datetime_date

from jobs.food_providers.food_providers import FoodProvider
from model.nutritional_constraints import NutritionalConstraints


class MealPlanRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True,
                              frozen=True)

    date: datetime_date
    nutritional_constraints: NutritionalConstraints
    food_blacklist: list[str] = []
    max_food_repeat: Optional[PositiveInt] = None
    food_provider: FoodProvider
