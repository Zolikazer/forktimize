from datetime import date
import pytest
from sqlmodel import SQLModel, create_engine, Session
from model.food import Food
from repository.forktimize_repository import get_unique_dates_after, get_foods_for_given_date

# 🔥 Create an in-memory SQLite test database
test_engine = create_engine("sqlite:///:memory:", echo=True)


@pytest.fixture(scope="function")
def test_db():
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="function")
def test_session(test_db):
    with Session(test_db) as session:
        yield session
        session.rollback()


def test_get_unique_dates_after(test_session):
    """Test that unique dates are correctly retrieved."""
    test_session.add_all([
        Food(food_id=1, date=date(2025, 3, 18), name="Chicken", calories=200, protein=30, carb=5, fat=10, price=5),
        Food(food_id=2, date=date(2025, 3, 19), name="Beef", calories=300, protein=40, carb=3, fat=15, price=7),
        Food(food_id=3, date=date(2025, 3, 19), name="Beef", calories=300, protein=40, carb=3, fat=15, price=7),
        Food(food_id=4, date=date(2025, 3, 20), name="Fish", calories=250, protein=35, carb=2, fat=12, price=6),
    ])
    test_session.commit()

    result = get_unique_dates_after(test_session, date(2025, 3, 18))
    assert result == [date(2025, 3, 19), date(2025, 3, 20)]


def test_get_foods_for_given_date(test_session):
    test_session.add_all([
        Food(food_id=1, date=date(2025, 3, 18), name="Chicken Salad", calories=200, protein=30, carb=5, fat=10,
             price=5),
        Food(food_id=2, date=date(2025, 3, 18), name="Beef Steak", calories=300, protein=40, carb=3, fat=15, price=7),
        Food(food_id=3, date=date(2025, 3, 18), name="Vegetable Pizza", calories=400, protein=15, carb=50, fat=20,
             price=8),
        Food(food_id=4, date=date(2025, 3, 19), name="Salmon", calories=350, protein=45, carb=0, fat=18, price=10),
    ])
    test_session.commit()

    foods = get_foods_for_given_date(test_session, date(2025, 3, 18))
    assert len(foods) == 3
    assert {food.name for food in foods} == {"Chicken Salad", "Beef Steak", "Vegetable Pizza"}

    foods = get_foods_for_given_date(test_session, date(2025, 3, 18), ["Pizza"])
    assert len(foods) == 2
    assert {food.name for food in foods} == {"Chicken Salad", "Beef Steak"}

    foods = get_foods_for_given_date(test_session, date(2025, 3, 20))
    assert len(foods) == 0

    foods = get_foods_for_given_date(test_session, date(2025, 3, 18), ["Beef", "Pizza"])
    assert len(foods) == 1
    assert {food.name for food in foods} == {"Chicken Salad"}
