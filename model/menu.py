from typing import List

from model.food import Food


class Menu:
    def __init__(self, foods: List[Food]):
        self.foods = foods

    @property
    def total_calories(self) -> int:
        return sum(food.kcal for food in self.foods)

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
        return sum(food.carbs for food in self.foods)

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
            "Chicken (g)": round(chicken_grams, 1),
            "Sugar (g)": round(sugar_grams, 1),
            "Olive Oil (g)": round(oil_grams, 1)
        }

    def __repr__(self):
        food_names = ',\n '.join(food.name for food in self.foods)
        return (
            f"Menu(foods=[\n{food_names}\n]\ntotal_calories={self.total_calories}\ntotal_protein={self.total_protein}\n"
            f"total_price={self.total_price}\ntotal_fat={self.total_fat}\ntotal_carbs={self.total_carbs}\n"
            f"price_per_calorie={self.price_per_calorie}\nprice_per_protein={self.price_per_protein}\n)")
