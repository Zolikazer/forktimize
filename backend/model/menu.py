from typing import List, ClassVar

from pydantic import BaseModel, ConfigDict, Field

from model.food import Food


class Menu(BaseModel):
    CHICKEN_PROTEIN_RATIO: ClassVar[float] = 25.0
    CHICKEN_FAT_RATIO: ClassVar[float] = 3.0

    foods: List[Food] = Field(default_factory=list)
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
        chicken_grams = (self.total_protein / self.CHICKEN_PROTEIN_RATIO) * 100.0
        chicken_fat = (chicken_grams / 100.0) * self.CHICKEN_FAT_RATIO
        leftover_fat = max(0, self.total_fat - int(chicken_fat))

        return {
            "Chicken (g)": int(chicken_grams),
            "Sugar (g)": self.total_carbs,
            "Olive Oil (g)": int(leftover_fat),
        }
