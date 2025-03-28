from __future__ import annotations

from datetime import date as date_type
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel

from model.food import Food
from model.food_log_entry import FoodLogEntry


class Menu(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel)

    foods: list[Food] = Field(default_factory=list)
    date: date_type = None

    @computed_field
    @property
    def food_log_entry(self) -> FoodLogEntry:
        return FoodLogEntry.from_macros(
            protein=self.total_protein,
            carb=self.total_carbs,
            fat=self.total_fat
        )

    @computed_field
    @property
    def total_price(self) -> int:
        return sum(food.price for food in self.foods)

    @computed_field
    @property
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
    def from_food_counts(cls, foods: list[Food], food_counts: dict[int, int], menu_date: date_type) -> Menu:
        id_to_food = {f.food_id: f for f in foods}
        selected = [
            id_to_food[food_id]
            for food_id, count in food_counts.items()
            for _ in range(count)
        ]
        return cls(foods=selected, date=menu_date)
