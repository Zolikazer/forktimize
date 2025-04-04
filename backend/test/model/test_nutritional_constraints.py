import pytest

from error_handling.exceptions import MealPlanRequestException
from model.nutritional_constraints import NutritionalConstraints


def test_valid_constraints():
    constraints = NutritionalConstraints(
        min_calories=1200,
        max_calories=2000,
        min_protein=50,
    )
    assert constraints.min_calories == 1200
    assert constraints.max_calories == 2000
    assert constraints.min_protein == 50


def test_invalid_constraints():
    with pytest.raises(ValueError):
        NutritionalConstraints(
            min_calories=-100,
            max_calories=2000,
            min_protein=50,
        )


def test_invalid_calorie_range():
    with pytest.raises(MealPlanRequestException) as e:
        NutritionalConstraints(
            min_calories=1200,
            max_calories=1000,
        )

    assert e.value.error_code == "max_lower_than_min"
    assert e.value.field == "calories"


def test_invalid_protein_range():
    with pytest.raises(MealPlanRequestException) as e:
        NutritionalConstraints(
            min_protein=50,
            max_protein=10
        )
    assert e.value.error_code == "max_lower_than_min"
    assert e.value.field == "protein"


def test_invalid_carb_range():
    with pytest.raises(MealPlanRequestException) as e:
        NutritionalConstraints(
            min_carb=50,
            max_carb=10
        )
    assert e.value.error_code == "max_lower_than_min"
    assert e.value.field == "carb"


def test_invalid_fat_range():
    with pytest.raises(MealPlanRequestException) as e:
        NutritionalConstraints(
            min_fat=50,
            max_fat=10
        )
    assert e.value.error_code == "max_lower_than_min"
    assert e.value.field == "fat"


def test_min_macros_calories_bigger_than_max_calories():
    with pytest.raises(MealPlanRequestException) as e:
        NutritionalConstraints(
            max_calories=1000,
            min_fat=9999,
            max_fat=99999
        )
    assert e.value.error_code == "macro_calories_conflict"
    assert e.value.field == "min"
