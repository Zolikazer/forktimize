from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from model.food import Food
from model.food_log_entry import FoodLogEntry


class Menu(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel)

    CHICKEN_PROTEIN_RATIO: ClassVar[float] = 25.0
    CHICKEN_FAT_RATIO: ClassVar[float] = 3.0

    foods: list[Food] = Field(default_factory=list)
    food_log_entry: FoodLogEntry = FoodLogEntry()

    def model_post_init(self, __context):
        self.food_log_entry = FoodLogEntry.from_macros(
            protein=self.total_protein,
            carb=self.total_carbs,
            fat=self.total_fat
        )

    def add_food(self, food: Food):
        self.foods.append(food)
        self.food_log_entry = FoodLogEntry.from_macros(
            protein=self.total_protein,
            carb=self.total_carbs,
            fat=self.total_fat
        )

    def add_foods(self, foods: list[Food]):
        self.foods.extend(foods)

        self.food_log_entry = FoodLogEntry.from_macros(
            protein=self.total_protein,
            carb=self.total_carbs,
            fat=self.total_fat
        )

    @property
    def total_calories(self) -> int:
        return sum(food.calories for food in self.foods)

    @property
    def total_protein(self) -> int:
        return sum(food.protein for food in self.foods)

    @property
    def total_price(self) -> int:
        return sum(food.price for food in self.foods)

    @property
    def total_fat(self) -> int:
        return sum(food.fat for food in self.foods)

    @property
    def total_carbs(self) -> int:
        return sum(food.carb for food in self.foods)

    @property
    def price_per_calorie(self) -> float:
        return 0 if self.total_calories == 0 else round(self.total_price / self.total_calories, 2)

    @property
    def price_per_protein(self) -> float:
        return 0 if self.total_protein == 0 else round(self.total_price / self.total_protein, 2)

    @staticmethod
    def from_food_counts(foods: list[Food], food_counts: dict[int, int]) -> Menu:
        id_to_food = {f.food_id: f for f in foods}
        selected = [
            id_to_food[food_id]
            for food_id, count in food_counts.items()
            for _ in range(count)
        ]
        return Menu(foods=selected)