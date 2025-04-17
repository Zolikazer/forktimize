from datetime import date

import pytest
from sqlmodel import SQLModel, create_engine, Session

from database.data_access import get_unique_dates_after, get_foods_for_given_date, is_database_empty, \
    get_available_dates_for_vendor
from food_vendors import food_vendor
from food_vendors.food_vendor_type import FoodVendorType
from model.food import Food
from test.conftest import make_food


@pytest.fixture(scope="function")
def test_db():
    test_engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="function")
def session(test_db):
    with Session(test_db) as session:
        yield session
        session.rollback()


@pytest.fixture(autouse=True)
def seed_db_with_foods(session):
    session.add_all([
        make_food(food_id=1, date=date(2025, 3, 18)),
        make_food(food_id=2, date=date(2025, 3, 18)),
        make_food(food_id=3, date=date(2025, 3, 18)),
        make_food(food_id=4, date=date(2025, 3, 19)),
        make_food(food_id=5, date=date(2025, 3, 20), food_vendor=FoodVendorType.INTER_FOOD),
    ])
    session.commit()


def test_get_foods_for_given_date__returns_all_cityfood_on_matching_date(session):
    foods = get_foods_for_given_date(session, date(2025, 3, 18), FoodVendorType.CITY_FOOD)
    assert len(foods) == 3
    assert {f.name for f in foods} == {"Test Chicken 1", "Test Chicken 2", "Test Chicken 3"}


def test_get_foods_for_given_date__returns_empty_list_if_vendor_has_no_food(session):
    foods = get_foods_for_given_date(session, date(2025, 3, 20), FoodVendorType.CITY_FOOD)
    assert foods == []


def test_get_foods_for_given_date__filters_out_blacklisted_foods(session):
    foods = get_foods_for_given_date(
        session,
        date(2025, 3, 18),
        FoodVendorType.CITY_FOOD,
        ["Test Chicken 1", "Test Chicken 2"]
    )
    assert len(foods) == 1
    assert foods[0].name == "Test Chicken 3"


def test_get_foods_for_given_date__returns_interfood_correctly(session):
    foods = get_foods_for_given_date(session, date(2025, 3, 20), FoodVendorType.INTER_FOOD)
    assert len(foods) == 1
    assert foods[0].name == "Test Chicken 5"


def test_get_unique_dates_after__returns_distinct_future_dates(session):
    session.add_all([
        make_food(date=date(2025, 3, 18)),
        make_food(date=date(2025, 3, 19)),
        make_food(date=date(2025, 3, 19)),
        make_food(date=date(2025, 3, 20)),
    ])

    session.commit()

    result = get_unique_dates_after(session, date(2025, 3, 18))
    assert result == [date(2025, 3, 19), date(2025, 3, 20)]


def test_get_available_dates_for_vendor__returns_distinct_future_dates(session):
    session.add_all([
        make_food(date=date(2025, 3, 18), food_vendor=FoodVendorType.CITY_FOOD),
        make_food(date=date(2025, 3, 19), food_vendor=FoodVendorType.CITY_FOOD),
        make_food(date=date(2025, 3, 19), food_vendor=FoodVendorType.CITY_FOOD),
        make_food(date=date(2025, 3, 20), food_vendor=FoodVendorType.CITY_FOOD),
        make_food(date=date(2025, 3, 20), food_vendor=FoodVendorType.INTER_FOOD),

    ])

    session.commit()

    result = get_available_dates_for_vendor(session, date(2025, 3, 18), FoodVendorType.CITY_FOOD)
    assert result == [date(2025, 3, 19), date(2025, 3, 20)]

def test_is_database_empty__returns_true_when_empty(session):
    session.query(Food).delete()
    assert is_database_empty(session) is True


def test_is_database_empty__returns_false_when_food_exists(session):
    assert is_database_empty(session) is False
