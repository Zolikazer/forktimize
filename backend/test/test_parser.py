import unittest
from datetime import datetime
from pathlib import Path

from model.food import Food
from data.parser import categorize_foods_by_date, parse_json, filter_out_food


class TestFoodParser(unittest.TestCase):
    def setUp(self):
        self.test_file = str(Path(__file__).parent.resolve() / "resources/city-response-test.json")
        self.example_foods = [
            Food(food_id=1, name="Tejszínes meggyleves", kcal=205, protein=2, carbs=39, fat=4, price=1475,
                 date=datetime(2025, 2, 19)),
            Food(food_id=2, name="Gulyásleves", kcal=300, protein=15, carbs=20, fat=10, price=2000,
                 date=datetime(2025, 2, 19)),
            Food(food_id=13, name="Rántott hús", kcal=400, protein=30, carbs=50, fat=20, price=2500,
                 date=datetime(2025, 2, 20))
        ]

    def test_parse_json_parses_all_foods(self):
        foods = parse_json(self.test_file)
        self.assertEqual(15, len(foods))

    def test_food_attributes(self):
        foods = parse_json(self.test_file)
        food = foods[0]
        self.assertEqual(food.name, "Thai marha üvegtésztával")
        self.assertEqual(food.kcal, 620)
        self.assertEqual(food.protein, 31)
        self.assertEqual(food.carbs, 101)
        self.assertEqual(food.fat, 9)
        self.assertEqual(food.price, 2130)
        self.assertEqual(food.date, datetime(2025, 2, 17))

    def test_categorize_foods_by_date(self):
        categorized_foods = categorize_foods_by_date(self.example_foods)

        self.assertEqual(len(categorized_foods), 2)
        self.assertEqual(len(categorized_foods["2025-02-19"]), 2)
        self.assertEqual(len(categorized_foods["2025-02-20"]), 1)
        self.assertEqual(categorized_foods["2025-02-19"][0].name, "Tejszínes meggyleves")
        self.assertEqual(categorized_foods["2025-02-19"][1].name, "Gulyásleves")
        self.assertEqual(categorized_foods["2025-02-20"][0].name, "Rántott hús")

    def test_filter_out_food(self):
        filtered_foods = filter_out_food(["Gulyásleves", "hús"], self.example_foods)
        self.assertEqual(len(filtered_foods), 1)
        self.assertEqual(filtered_foods[0].name, "Tejszínes meggyleves")
