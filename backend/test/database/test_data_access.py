from datetime import date
import pytest
from sqlmodel import SQLModel, create_engine, Session

from database.data_access import get_unique_dates_after, get_foods_for_given_date, is_database_empty
from model.food import Food, FoodProvider
from test.food_factory import make_food

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
    test_session.add_all([
        make_food(date=date(2025, 3, 18)),
        make_food(date=date(2025, 3, 19)),
        make_food(date=date(2025, 3, 19)),
        make_food(date=date(2025, 3, 20)),
    ])

    test_session.commit()

    result = get_unique_dates_after(test_session, date(2025, 3, 18))
    assert result == [date(2025, 3, 19), date(2025, 3, 20)]


def test_get_foods_for_given_date(test_session):
    test_session.add_all([
        make_food(food_id=1, date=date(2025, 3, 18)),
        make_food(food_id=2, date=date(2025, 3, 18)),
        make_food(food_id=3, date=date(2025, 3, 18)),
        make_food(food_id=4, date=date(2025, 3, 19)),
    ])
    test_session.commit()

    foods = get_foods_for_given_date(test_session, date(2025, 3, 18))
    assert len(foods) == 3
    assert {food.name for food in foods} == {"Test Chicken 1", "Test Chicken 2", "Test Chicken 3"}

    foods = get_foods_for_given_date(test_session, date(2025, 3, 18), ["Test Chicken 3"])
    assert len(foods) == 2
    assert {food.name for food in foods} == {"Test Chicken 1", "Test Chicken 2"}

    foods = get_foods_for_given_date(test_session, date(2025, 3, 20))
    assert len(foods) == 0

    foods = get_foods_for_given_date(test_session, date(2025, 3, 18),
                                     ["Test Chicken 1", "Test Chicken 2"])
    assert len(foods) == 1
    assert {food.name for food in foods} == {"Test Chicken 3"}


def test_is_database_empty_when_no_food(test_session):
    assert is_database_empty(test_session) is True


def test_is_database_empty_when_food_exists(test_session):
    test_session.add_all([
        make_food()
    ])
    assert is_database_empty(test_session) is False
