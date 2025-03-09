from unittest import TestCase

import pytest

from model.nutritional_constraints import NutritionalConstraints, to_camel


class TestNutritionalConstraints(TestCase):

    def test_valid_constraints(self):
        constraints = NutritionalConstraints(
            min_calories=1200,
            max_calories=2000,
            min_protein=50,
            max_occurrences_per_food=10
        )
        self.assertEqual(constraints.min_calories, 1200)
        self.assertEqual(constraints.max_calories, 2000)
        self.assertEqual(constraints.min_protein, 50)
        self.assertEqual(constraints.max_occurrences_per_food, 10)

    def test_invalid_constraints(self):
        with self.assertRaises(ValueError):
            NutritionalConstraints(
                min_calories=-100,
                max_calories=2000,
                min_protein=50,
                max_items=10
            )

    def test_invalid_calorie_range(self):
        with self.assertRaises(ValueError):
            NutritionalConstraints(
                min_calories=1200,
                max_calories=1000,
            )

    def test_invalid_protein_range(self):
        with self.assertRaises(ValueError):
            NutritionalConstraints(
                min_protein=50,
                max_protein=10
            )

    def test_invalid_carb_range(self):
        with self.assertRaises(ValueError):
            NutritionalConstraints(
                min_carb=50,
                max_carb=10
            )

    def test_invalid_fat_range(self):
        with self.assertRaises(ValueError):
            NutritionalConstraints(
                min_fat=50,
                max_fat=10
            )

    def test_min_macros_lower_than_max_calories(self):
        with self.assertRaises(ValueError):
            NutritionalConstraints(
                max_calories=1000,
                min_fat=9999,
                max_fat=10
            )
