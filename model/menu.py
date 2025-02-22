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
        return round(self.total_price / self.total_calories, 2)

    @property
    def price_per_protein(self) -> float:
        return round(self.total_price / self.total_protein, 2)

    def __repr__(self):
        food_names = ', '.join(food.name for food in self.foods)
        return (f"Menu(foods=[{food_names}], total_calories={self.total_calories}, total_protein={self.total_protein}, "
                f"total_price={self.total_price}, total_fat={self.total_fat}, total_carbs={self.total_carbs}, "
                f"price_per_calorie={self.price_per_calorie}, price_per_protein={self.price_per_protein})")
