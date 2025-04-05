from datetime import date as datetime_date

from pydantic import ConfigDict, NonNegativeInt, StrictInt
from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel, Field

from model.food_providers import FoodProvider


class Food(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel)

    food_id: StrictInt = Field(primary_key=True)
    date: datetime_date = Field(primary_key=True, index=True)
    food_provider: FoodProvider = Field(
        primary_key=True,
        nullable=False,
        index=True
    )
    name: str = Field(index=True)
    calories: NonNegativeInt
    protein: NonNegativeInt
    carb: NonNegativeInt
    fat: NonNegativeInt
    price: NonNegativeInt

    @property
    def price_per_kcal(self):
        return round(self.price / self.calories, 2)

    @property
    def price_per_protein(self):
        return 0 if self.protein == 0 else round(self.price / self.protein, 2)

    @property
    def kcal_per_protein(self):
        return 0 if self.protein == 0 else round(self.calories / self.protein, 2)

    def __hash__(self):
        return hash((self.food_id, self.date, self.food_provider))

    def __eq__(self, other):
        if not isinstance(other, Food):
            return NotImplemented
        return (
            self.food_id == other.food_id and
            self.date == other.date and
            self.food_provider == other.food_provider
        )