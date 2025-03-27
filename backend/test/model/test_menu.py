from datetime import date
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
        date=date(2025, 3, 7)
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
        date=date.today()
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


def test_menu_from_food_counts():
    apple_id = 1
    chicken_id = 2
    menu_date = date.today()
    foods = [
        Food(food_id=apple_id, name="Apple", price=1.0, calories=50, protein=0.5, carb=14, fat=0.2),
        Food(food_id=chicken_id, name="Chicken", price=3.0, calories=200, protein=30, carb=0, fat=5),
    ]
    food_counts = {
        apple_id: 2,
        chicken_id: 1
    }

    menu = Menu.from_food_counts(foods, food_counts, menu_date)

    assert len(menu.foods) == 3

    names = [f.name for f in menu.foods]
    assert names.count("Apple") == 2
    assert names.count("Chicken") == 1

    food_ids = [f.food_id for f in menu.foods]
    assert set(food_ids).issubset({apple_id, chicken_id})
    assert menu.date == menu_date