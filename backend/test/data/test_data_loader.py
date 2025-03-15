import unittest
from datetime import datetime, date
from pathlib import Path

from data.serialization import load_food_from_json
from model.food import Food


class TestFoodParser(unittest.TestCase):
    def setUp(self):
        self.test_file = str(Path(__file__).parent.parent.resolve() / "resources/city-response-test.json")
        self.example_foods = [
            Food(food_id=1, name="Tejszínes meggyleves", calories=205, protein=2, carb=39, fat=4, price=1475,
                 date=datetime(2025, 2, 19)),
            Food(food_id=2, name="Gulyásleves", calories=300, protein=15, carb=20, fat=10, price=2000,
                 date=datetime(2025, 2, 19)),
            Food(food_id=13, name="Rántott hús", calories=400, protein=30, carb=50, fat=20, price=2500,
                 date=datetime(2025, 2, 20))
        ]

    def test_parse_json_parses_all_foods(self):
        foods = load_food_from_json(self.test_file)
        self.assertEqual(15, len(foods))

    def test_food_attributes(self):
        foods = load_food_from_json(self.test_file)
        food = foods[0]
        self.assertEqual(food.name, "Thai marha üvegtésztával")
        self.assertEqual(food.calories, 620)
        self.assertEqual(food.protein, 31)
        self.assertEqual(food.carb, 101)
        self.assertEqual(food.fat, 9)
        self.assertEqual(food.price, 2130)
        self.assertEqual(food.date, date(2025, 2, 17))
