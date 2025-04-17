from datetime import date as datetime_date

from pydantic import ConfigDict, NonNegativeInt, StrictInt
from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel, Field

from food_vendors.food_vendor_type import FoodVendorType


class Food(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True)

    food_id: StrictInt = Field(primary_key=True, nullable=False)
    date: datetime_date = Field(primary_key=True, index=True, nullable=False)
    food_vendor: FoodVendorType = Field(
        primary_key=True,
        nullable=False,
        index=True
    )
    name: str = Field(index=True, nullable=False, min_length=1)
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
        return hash((self.food_id, self.date, self.food_vendor))

    def __eq__(self, other):
        if not isinstance(other, Food):
            return NotImplemented
        return (
                self.food_id == other.food_id and
                self.date == other.date and
                self.food_vendor == other.food_vendor
        )