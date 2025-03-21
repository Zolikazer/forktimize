import datetime

import pytest

from model.food import Food
from model.food_log_entry import FoodLogEntry
from model.menu import Menu


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
        date=datetime.datetime(2025, 3, 7)
    )


def test_menu_creation():
    menu = Menu()
    assert menu.foods == []


def test_add_food(sample_food):
    menu = Menu()
    menu.add_food(sample_food)

    assert len(menu.foods) == 1
    assert menu.foods[0] == sample_food


def test_add_foods(sample_food):
    menu = Menu()
    menu.add_foods([sample_food, sample_food, sample_food])

    assert len(menu.foods) == 3
    assert menu.foods[0] == sample_food


def test_total_calories(sample_food):
    menu = Menu()
    menu.add_food(sample_food)
    menu.add_food(sample_food)

    assert menu.total_calories == sample_food.calories * 2


def test_total_protein(sample_food):
    menu = Menu()
    menu.add_food(sample_food)

    assert menu.total_protein == sample_food.protein


def test_total_price(sample_food):
    menu = Menu()
    menu.add_food(sample_food)

    assert menu.total_price == sample_food.price


def test_total_fat(sample_food):
    menu = Menu()
    menu.add_food(sample_food)

    assert menu.total_fat == sample_food.fat


def test_total_carbs(sample_food):
    menu = Menu()
    menu.add_food(sample_food)

    assert menu.total_carbs == sample_food.carb


def test_price_per_calorie(sample_food):
    menu = Menu()
    menu.add_food(sample_food)

    expected_price_per_kcal = round(sample_food.price / sample_food.calories, 2)
    assert menu.price_per_calorie == expected_price_per_kcal

    empty_menu = Menu()
    assert empty_menu.price_per_calorie == 0


def test_price_per_protein(sample_food):
    menu = Menu()
    menu.add_food(sample_food)

    expected_price_per_protein = round(sample_food.price / sample_food.protein, 2)
    assert menu.price_per_protein == expected_price_per_protein

    food_no_protein = Food(
        food_id=2,
        name="Zero Protein Food",
        calories=100,
        protein=0,
        carb=10,
        fat=5,
        price=300,
        date=datetime.datetime.now()
    )

    menu_no_protein = Menu()
    menu_no_protein.add_food(food_no_protein)

    assert menu_no_protein.price_per_protein == 0


def test_menu_initializes_food_log_entry(sample_food):
    foods = [sample_food, sample_food]

    menu = Menu(foods=foods)

    assert isinstance(menu.food_log_entry, FoodLogEntry)
    assert menu.food_log_entry.chicken == 320
    assert menu.food_log_entry.sugar == 10
    assert menu.food_log_entry.oil == 0
