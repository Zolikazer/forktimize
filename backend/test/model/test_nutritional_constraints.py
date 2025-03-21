import pytest
from model.nutritional_constraints import NutritionalConstraints


def test_valid_constraints():
    constraints = NutritionalConstraints(
        min_calories=1200,
        max_calories=2000,
        min_protein=50,
        max_occurrences_per_food=10
    )
    assert constraints.min_calories == 1200
    assert constraints.max_calories == 2000
    assert constraints.min_protein == 50
    assert constraints.max_occurrences_per_food == 10


def test_invalid_constraints():
    with pytest.raises(ValueError):
        NutritionalConstraints(
            min_calories=-100,
            max_calories=2000,
            min_protein=50,
            max_items=10
        )


def test_invalid_calorie_range():
    with pytest.raises(ValueError):
        NutritionalConstraints(
            min_calories=1200,
            max_calories=1000,
        )


def test_invalid_protein_range():
    with pytest.raises(ValueError):
        NutritionalConstraints(
            min_protein=50,
            max_protein=10
        )


def test_invalid_carb_range():
    with pytest.raises(ValueError):
        NutritionalConstraints(
            min_carb=50,
            max_carb=10
        )


def test_invalid_fat_range():
    with pytest.raises(ValueError):
        NutritionalConstraints(
            min_fat=50,
            max_fat=10
        )


def test_min_macros_lower_than_max_calories():
    with pytest.raises(ValueError):
        NutritionalConstraints(
            max_calories=1000,
            min_fat=9999,
            max_fat=10
        )
