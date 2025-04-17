from datetime import date

import pytest
from pydantic import ValidationError

from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.teletal.food_model_mapper import map_to_food_model


@pytest.fixture
def raw_food_data():
    def _make(**overrides):
        base = {
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
        base.update(overrides)
        return base

    return _make


def test_map_to_food_model__converts_raw_dict_to_valid_food_instance(raw_food_data):
    food = map_to_food_model(raw_food_data())

    assert food.food_id == 941378554296
    assert food.name == "Zabkása eperöntettel"
    assert food.date == date(2025, 4, 7)
    assert food.food_vendor == FoodVendorType.TELETAL
    assert food.calories == 262
    assert food.protein == 11
    assert food.carb == 26
    assert food.fat == 11
    assert food.price == 395
    assert isinstance(food.food_id, int)
    assert len(str(food.food_id)) == 12


def test_map_to_food_model__parses_price_string_with_thousand_separator_correctly(raw_food_data):
    food = map_to_food_model(raw_food_data(price="1.990 Ft"))
    assert food.price == 1990


def test_map_to_food_model__parses_calories_string_with_4_digit_value(raw_food_data):
    food = map_to_food_model(raw_food_data(calories="1,262.10 kcal"))
    assert food.calories == 1262


def test_map_to_food_model__raises_exception_if_model_invalid(raw_food_data):
    with pytest.raises(ValidationError):
        map_to_food_model(raw_food_data(name=""))
