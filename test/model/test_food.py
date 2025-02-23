from datetime import datetime
from unittest import TestCase

from model.food import Food


class TestFood(TestCase):
    def test_something(self):
        food = Food(name="Valami", protein=128, kcal=85, fat=98, price=2000, carbs=100,
                    date=datetime.strptime("2025-12-07", "%Y-%m-%d"))
        self.assertEqual(food.name, "Valami")
        self.assertEqual(food.protein, 128)
        self.assertEqual(food.kcal, 85)
        self.assertEqual(food.price, 2000)
        self.assertEqual(food.fat, 98)
        self.assertEqual(food.carbs, 100)
        self.assertEqual(food.date, datetime(2025, 12, 7))
