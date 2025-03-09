import datetime

import pytest

from model.food import Food
from model.menu import Menu


@pytest.fixture
def sample_food():
    """Fixture to provide a sample food object."""
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
    """Test that a Menu object initializes correctly."""
    menu = Menu()
    assert menu.foods == []


def test_add_food(sample_food):
    """Test that adding food to the menu works correctly."""
    menu = Menu()
    menu.add_food(sample_food)

    assert len(menu.foods) == 1
    assert menu.foods[0] == sample_food


def test_total_calories(sample_food):
    """Test that total_calories property sums correctly."""
    menu = Menu()
    menu.add_food(sample_food)
    menu.add_food(sample_food)  # Add same food twice

    assert menu.total_calories == sample_food.calories * 2


def test_total_protein(sample_food):
    """Test that total_protein property sums correctly."""
    menu = Menu()
    menu.add_food(sample_food)

    assert menu.total_protein == sample_food.protein


def test_total_price(sample_food):
    """Test that total_price property sums correctly."""
    menu = Menu()
    menu.add_food(sample_food)

    assert menu.total_price == sample_food.price


def test_total_fat(sample_food):
    """Test that total_fat property sums correctly."""
    menu = Menu()
    menu.add_food(sample_food)

    assert menu.total_fat == sample_food.fat


def test_total_carbs(sample_food):
    """Test that total_carbs property sums correctly."""
    menu = Menu()
    menu.add_food(sample_food)

    assert menu.total_carbs == sample_food.carb


def test_price_per_calorie(sample_food):
    """Test price per calorie calculation."""
    menu = Menu()
    menu.add_food(sample_food)

    expected_price_per_kcal = round(sample_food.price / sample_food.calories, 2)
    assert menu.price_per_calorie == expected_price_per_kcal

    # Edge case: No food in menu (should return 0)
    empty_menu = Menu()
    assert empty_menu.price_per_calorie == 0


def test_price_per_protein(sample_food):
    """Test price per protein calculation."""
    menu = Menu()
    menu.add_food(sample_food)

    expected_price_per_protein = round(sample_food.price / sample_food.protein, 2)
    assert menu.price_per_protein == expected_price_per_protein

    # Edge case: No protein in menu (should return 0)
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


def test_to_myfitnesspal_entries():
    """Test conversion to MyFitnessPal entries."""
    menu = Menu()

    menu.add_food(Food(food_id=1, name="Chicken", calories=400, protein=50, carb=20, fat=10, price=800,
                       date=datetime.datetime.now()))
    menu.add_food(
        Food(food_id=2, name="Rice", calories=300, protein=5, carb=60, fat=1, price=200, date=datetime.datetime.now()))

    entries = menu.to_myfitnesspal_entries()

    assert entries["Chicken (g)"] == 220
    assert entries["Sugar (g)"] == menu.total_carbs
    assert entries["Olive Oil (g)"] == 5
