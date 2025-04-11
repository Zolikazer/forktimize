from datetime import date

from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.teletal.food_model_mapper import map_to_food_model


def test_to_food_model_parses_data_correctly():
    food_data = {
        "name": "Zabkása eperöntettel",
        "year": "2025",
        "week": "15",
        "day": "1",
        "calories": "262.10 kcal",
        "protein": "11.30 g",
        "carb": "26.20 g",
        "fat": "11.5 g",
        "price": "395 Ft"
    }

    food = map_to_food_model(food_data)

    assert food.name == "Zabkása eperöntettel"
    assert food.date == date(2025, 4, 7)
    assert food.food_vendor == FoodVendor.TELETAL
    assert food.calories == 262
    assert food.protein == 11
    assert food.carb == 26
    assert food.fat == 11
    assert food.price == 395
    assert isinstance(food.food_id, int)
    assert len(str(food.food_id)) == 12


def test_to_food_model_parses_data_correctly_with_thousand_seperator():
    food_data = {
        "name": "Zabkása eperöntettel\nBanán",
        "year": "2025",
        "week": "18",
        "day": "5",
        "calories": "1,053.50 kcal",
        "protein": "11.30 g",
        "carb": "26.20 g",
        "fat": "11.50 g",
        "price": "1.990 Ft"
    }

    food = map_to_food_model(food_data)

    assert food.name == "Zabkása eperöntettel\nBanán"
    assert food.date == date(2025, 5, 2)
    assert food.food_vendor == FoodVendor.TELETAL
    assert food.calories == 1053
    assert food.protein == 11
    assert food.carb == 26
    assert food.fat == 11
    assert food.price == 1990
    assert isinstance(food.food_id, int)
    assert len(str(food.food_id)) == 12
