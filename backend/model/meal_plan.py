from __future__ import annotations

from datetime import date as datetime_date

from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel

from model.food import Food
from food_vendors.food_vendor import FoodVendor
from model.food_log_entry import FoodLogEntry


class MealPlan(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True)

    foods: list[Food] = Field(default_factory=list)
    date: datetime_date = None
    food_vendor: FoodVendor = None

    @computed_field
    def food_log_entry(self) -> FoodLogEntry:
        return FoodLogEntry.from_macros(
            protein=self.total_protein,
            carb=self.total_carbs,
            fat=self.total_fat
        )

    @computed_field
    def total_price(self) -> int:
        return sum(food.price for food in self.foods)

    @computed_field
    def total_calories(self) -> int:
        return sum(food.calories for food in self.foods)

    @computed_field
    @property
    def total_protein(self) -> int:
        return sum(food.protein for food in self.foods)

    @computed_field
    @property
    def total_carbs(self) -> int:
        return sum(food.carb for food in self.foods)

    @computed_field
    @property
    def total_fat(self) -> int:
        return sum(food.fat for food in self.foods)

    @property
    def price_per_calorie(self) -> float:
        return 0 if self.total_calories == 0 else round(self.total_price / self.total_calories, 2)

    @property
    def price_per_protein(self) -> float:
        return 0 if self.total_protein == 0 else round(self.total_price / self.total_protein, 2)

    def add_food(self, food: Food):
        self.foods.append(food)

    def add_foods(self, foods: list[Food]):
        self.foods.extend(foods)

    @classmethod
    def from_food_counts(cls, foods: list[Food], food_counts: dict[int, int], plan_date: datetime_date,
                         food_vendor: FoodVendor) -> MealPlan:
        id_to_food = {f.food_id: f for f in foods}
        selected = [
            id_to_food[food_id]
            for food_id, count in food_counts.items()
            for _ in range(count)
        ]
        return cls(foods=selected, date=plan_date, food_vendor=food_vendor)
