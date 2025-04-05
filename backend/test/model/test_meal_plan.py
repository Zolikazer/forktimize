from datetime import date

import pytest

from model.food import Food
from model.food_providers import FoodProvider
from model.food_log_entry import FoodLogEntry
from model.meal_plan import MealPlan


@pytest.fixture
def sample_food():
    return Food(
        food_id=1,
        name="Chicken Breast",
        calories=200,
        protein=40,
        carb=5,
        fat=3,
        price=500,
        date=date(2025, 3, 7)
    )


def test_meal_plan_generation():
    meal_plan = MealPlan()
    assert meal_plan.foods == []


def test_add_food(sample_food):
    meal_plan = MealPlan()
    meal_plan.add_food(sample_food)

    assert len(meal_plan.foods) == 1
    assert meal_plan.foods[0] == sample_food


def test_add_foods(sample_food):
    meal_plan = MealPlan()
    meal_plan.add_foods([sample_food, sample_food, sample_food])

    assert len(meal_plan.foods) == 3
    assert meal_plan.foods[0] == sample_food


def test_total_calories(sample_food):
    meal_plan = MealPlan()
    meal_plan.add_food(sample_food)
    meal_plan.add_food(sample_food)

    assert meal_plan.total_calories == sample_food.calories * 2


def test_total_protein(sample_food):
    meal_plan = MealPlan()
    meal_plan.add_food(sample_food)

    assert meal_plan.total_protein == sample_food.protein


def test_total_price(sample_food):
    meal_plan = MealPlan()
    meal_plan.add_food(sample_food)

    assert meal_plan.total_price == sample_food.price


def test_total_fat(sample_food):
    meal_plan = MealPlan()
    meal_plan.add_food(sample_food)

    assert meal_plan.total_fat == sample_food.fat


def test_total_carbs(sample_food):
    meal_plan = MealPlan()
    meal_plan.add_food(sample_food)

    assert meal_plan.total_carbs == sample_food.carb


def test_price_per_calorie(sample_food):
    meal_plan = MealPlan()
    meal_plan.add_food(sample_food)

    expected_price_per_kcal = round(sample_food.price / sample_food.calories, 2)
    assert meal_plan.price_per_calorie == expected_price_per_kcal

    empty_meal_plan = MealPlan()
    assert empty_meal_plan.price_per_calorie == 0


def test_price_per_protein(sample_food):
    meal_plan = MealPlan()
    meal_plan.add_food(sample_food)

    expected_price_per_protein = round(sample_food.price / sample_food.protein, 2)
    assert meal_plan.price_per_protein == expected_price_per_protein

    food_no_protein = Food(
        food_id=2,
        name="Zero Protein Food",
        calories=100,
        protein=0,
        carb=10,
        fat=5,
        price=300,
        date=date.today()
    )

    meal_plan_no_protein = MealPlan()
    meal_plan_no_protein.add_food(food_no_protein)

    assert meal_plan_no_protein.price_per_protein == 0


def test_meal_plan_initializes_food_log_entry(sample_food):
    foods = [sample_food, sample_food]

    meal_plan = MealPlan(foods=foods)

    assert isinstance(meal_plan.food_log_entry, FoodLogEntry)
    assert meal_plan.food_log_entry.chicken == 320
    assert meal_plan.food_log_entry.sugar == 10
    assert meal_plan.food_log_entry.oil == 0


def test_meal_plan_from_food_counts():
    apple_id = 1
    chicken_id = 2
    plan_date = date.today()
    foods = [
        Food(food_id=apple_id, name="Apple", price=1.0, calories=50, protein=0.5, carb=14, fat=0.2),
        Food(food_id=chicken_id, name="Chicken", price=3.0, calories=200, protein=30, carb=0, fat=5),
    ]
    food_counts = {
        apple_id: 2,
        chicken_id: 1
    }

    meal_plan = MealPlan.from_food_counts(foods, food_counts, plan_date, FoodProvider.CITY_FOOD)

    assert len(meal_plan.foods) == 3

    names = [f.name for f in meal_plan.foods]
    assert names.count("Apple") == 2
    assert names.count("Chicken") == 1

    food_ids = [f.food_id for f in meal_plan.foods]
    assert set(food_ids).issubset({apple_id, chicken_id})
    assert meal_plan.date == plan_date