from typing import List

from pydantic import BaseModel, ConfigDict

from model.food import Food


class Menu(BaseModel):
    foods: List[Food] = []
    model_config = ConfigDict(arbitrary_types_allowed=True)

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

    def add_food(self, food: Food):
        self.foods.append(food)

    def to_myfitnesspal_entries(self) -> dict:
        chicken_grams = (self.total_protein / 25.0) * 100.0
        chicken_fat = (chicken_grams / 100.0) * 3.0
        leftover_fat = self.total_fat - chicken_fat

        if leftover_fat < 0:
            leftover_fat = 0

        sugar_grams = self.total_carbs

        oil_grams = leftover_fat

        return {
            "Chicken (g)": int(chicken_grams),
            "Sugar (g)": int(sugar_grams),
            "Olive Oil (g)": int(oil_grams)
        }