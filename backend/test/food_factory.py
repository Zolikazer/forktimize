import itertools
from datetime import date as datetime_date
from functools import partial

from model.food import Food
from model.food_providers import FoodProvider

_food_id_counter = itertools.count(1)


def make_food(
        food_id: int = None,
        name: str = None,
        food_provider: FoodProvider = FoodProvider.CITY_FOOD,
        date: datetime_date = datetime_date(2025, 2, 24),
        calories: int = 500,
        protein: int = 50,
        carb: int = 50,
        fat: int = 11,
        price: int = 1000
) -> Food:
    if food_id is None:
        food_id = next(_food_id_counter)
    if name is None:
        name = f"Test Chicken {food_id}"

    return Food(
        food_id=food_id,
        name=name,
        food_provider=food_provider,
        date=date,
        calories=calories,
        protein=protein,
        carb=carb,
        fat=fat,
        price=price
    )


make_high_protein = partial(make_food, protein=80, calories=700)
make_low_carb = partial(make_food, carb=20)
make_cityfood = partial(make_food, food_provider=FoodProvider.CITY_FOOD)
