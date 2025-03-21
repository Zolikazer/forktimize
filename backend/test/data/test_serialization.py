import pytest
from datetime import date
from pathlib import Path
from data.serialization import load_food_from_json


@pytest.fixture
def test_file():
    return str(Path(__file__).parent.parent.resolve() / "resources/city-response-test.json")


def test_parse_json_parses_all_foods(test_file):
    foods = load_food_from_json(test_file)
    assert len(foods) == 15


def test_food_attributes(test_file):
    foods = load_food_from_json(test_file)
    food = foods[0]

    assert food.name == "Thai marha üvegtésztával"
    assert food.calories == 620
    assert food.protein == 31
    assert food.carb == 101
    assert food.fat == 9
    assert food.price == 2130
    assert food.date == date(2025, 2, 17)
