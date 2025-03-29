import datetime

from model.food import Food, FoodProvider


def test_food_creation():
    food = Food(
        food_id=1,
        name="Chicken Breast",
        calories=200,
        protein=40,
        carb=5,
        fat=3,
        price=500,
        date=datetime.datetime(2025, 3, 7)
    )

    assert food.food_id == 1
    assert food.name == "Chicken Breast"
    assert food.calories == 200
    assert food.protein == 40
    assert food.carb == 5
    assert food.fat == 3
    assert food.price == 500
    assert food.date == datetime.datetime(2025, 3, 7)


def test_price_per_kcal():
    food = Food(food_id=1, name="Test", calories=200, protein=40, carb=5, fat=3, price=500,
                date=datetime.datetime.now())
    assert food.price_per_kcal == round(500 / 200, 2)


def test_price_per_protein():
    food = Food(food_id=1, name="Test", calories=200, protein=40, carb=5, fat=3, price=500,
                date=datetime.datetime.now())
    assert food.price_per_protein == round(500 / 40, 2)

    food_no_protein = Food(food_id=2, name="Zero Protein Food", calories=150, protein=0, carb=10, fat=5, price=300,
                           date=datetime.datetime.now())
    assert food_no_protein.price_per_protein == 0


def test_kcal_per_protein():
    food = Food(food_id=1, name="Test", calories=200, protein=40, carb=5, fat=3, price=500,
                date=datetime.datetime.now())
    assert food.kcal_per_protein == round(200 / 40, 2)

    food_no_protein = Food(food_id=2, name="Zero Protein Food", calories=150, protein=0, carb=10, fat=5, price=300,
                           date=datetime.datetime.now())
    assert food_no_protein.kcal_per_protein == 0
    # sanity-check
