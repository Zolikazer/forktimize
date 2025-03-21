from datetime import date as datetime_date

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel, Field


class Food(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel)

    food_id: int = Field(primary_key=True)
    date: datetime_date = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    calories: int
    protein: int
    carb: int
    fat: int
    price: int

    @property
    def price_per_kcal(self):
        return round(self.price / self.calories, 2)

    @property
    def price_per_protein(self):
        return 0 if self.protein == 0 else round(self.price / self.protein, 2)

    @property
    def kcal_per_protein(self):
        return 0 if self.protein == 0 else round(self.calories / self.protein, 2)

    def __repr__(self):
        return (f"Food(name={self.name}, food_id={self.food_id} kcal={self.calories}, protein={self.protein}, "
                f"carbs={self.carb}, fat={self.fat}, price={self.price}, date={self.date}, "
                f"price_per_kcal={self.price_per_kcal}, kcal_per_protein={self.kcal_per_protein}, "
                f"price_per_protein={self.price_per_protein})")

    def __hash__(self):
        return hash(self.food_id)
