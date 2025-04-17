from datetime import date
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine, StaticPool
from sqlmodel import SQLModel, Session
from starlette.testclient import TestClient

from database.db import get_session
from food_vendors.food_vendor_type import FoodVendorType
from main import app
from routers.meal_planner import AppStatus
from test.conftest import make_food


@pytest.fixture(name="session")
def in_memory_session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def forktimize_client(session):
    app.dependency_overrides[get_session] = lambda: session
    return TestClient(app)


def make_meal_request(**overrides) -> dict:
    base = {
        "date": "2025-02-24",
        "nutritional_constraints": {
            "min_calories": 1500,
            "max_calories": 2700,
            "min_protein": 200
        },
        "food_blacklist": [],
        "food_vendor": "cityfood"
    }
    base.update(overrides)

    return base


@pytest.fixture(autouse=True)
def insert_test_food(session):
    food_items = [make_food(calories=500, protein=50, carb=20, fat=10, price=1000),
                  make_food(calories=600, protein=55, carb=10, fat=25, price=1200),
                  make_food(name="Lencsefőzelék vagdalttal", calories=400, protein=20, carb=50, fat=10, price=800),
                  make_food(calories=800, protein=70, carb=5, fat=40, price=2000),
                  make_food(calories=500, protein=15, carb=80, fat=5, price=800),
                  make_food(calories=500, protein=15, carb=80, fat=5, price=800, date=date(2025, 2, 25)),
                  make_food(calories=500, protein=15, carb=80, fat=5, price=800, date=date(2025, 2, 23))
                  ]

    session.add_all(food_items)
    session.commit()


def test_create_meal_plan__returns_correct_meal_plan(forktimize_client, session: Session):
    session.add(make_food(price=0, food_vendor=FoodVendorType.INTER_FOOD))

    meal_plan_request = make_meal_request()

    response = forktimize_client.post("/meal-plan", json=meal_plan_request)

    assert response.status_code == 200
    data = response.json()

    assert data["date"] == meal_plan_request["date"]
    assert len(data["foods"]) == 4

    assert data["totalPrice"] == 4000
    assert data["totalCalories"] == 2000
    assert data["totalProtein"] == 200
    assert data["totalCarbs"] == 80
    assert data["totalFat"] == 40
    assert data["foodVendor"] == "cityfood"


def test_create_meal_plan__returns_correct_food_log_entry(forktimize_client, session: Session):
    session.add(make_food(price=0, food_vendor=FoodVendorType.INTER_FOOD))

    response = forktimize_client.post("/meal-plan", json=make_meal_request())

    assert response.status_code == 200
    data = response.json()

    food_log_entry = data["foodLogEntry"]
    assert food_log_entry["chicken"] == 800
    assert food_log_entry["oil"] == 16
    assert food_log_entry["sugar"] == 80


def test_create_meal_plan__filters_blacklist(forktimize_client, session: Session):
    blacklisted_food = "cheap_and_blacklisted"
    session.add(make_food(name=blacklisted_food, price=0, food_vendor=FoodVendorType.CITY_FOOD))
    meal_plan_request = make_meal_request(**{"food_blacklist": [blacklisted_food]})

    response = forktimize_client.post("/meal-plan", json=meal_plan_request)

    assert response.status_code == 200
    data = response.json()

    assert blacklisted_food not in [f["name"] for f in data["foods"]]


def test_create_meal_plan__filters_food_by_food_provider(forktimize_client, session: Session):
    food_with_different_provider = make_food(price=0, food_vendor=FoodVendorType.INTER_FOOD)
    session.add(food_with_different_provider)
    meal_plan_request = make_meal_request()

    response = forktimize_client.post("/meal-plan", json=meal_plan_request)

    assert response.status_code == 200
    data = response.json()

    assert food_with_different_provider.name not in [f["name"] for f in data["foods"]]


def test_create_meal_plan__honors_max_food_repeat_limit(forktimize_client, session: Session):
    meal_planner_request = make_meal_request(**{"max_food_repeat": 1})

    response = forktimize_client.post("/meal-plan", json=meal_planner_request)

    assert response.status_code == 200
    data = response.json()

    food_names = [f["name"] for f in data["foods"]]
    name_counts = {name: food_names.count(name) for name in food_names}

    for name, count in name_counts.items():
        assert count == 1, f"Food '{name}' appears {count} times"


@freeze_time("2025-02-23")
def test_get_available_dates__returns_future_dates_only(forktimize_client, session):
    response = forktimize_client.get("/dates")

    assert response.status_code == 200
    assert response.json() == ["2025-02-24", "2025-02-25"]


def test_health_check__returns_status_healthy_when_db_connected(forktimize_client):
    response = forktimize_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "HEALTHY", "database": "connected"}


def test_health_check__returns_unhealthy_status_when_db_fails(forktimize_client):
    broken_session = MagicMock()
    broken_session.exec.side_effect = Exception("Database gone fishing 🐟")

    app.dependency_overrides = {
        get_session: lambda: broken_session
    }

    response = forktimize_client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": AppStatus.UNHEALTHY,
        "database": "error"
    }


def test_create_meal_plan__returns_422_if_min_macros_exceed_calories(forktimize_client):
    meal_planner_request = make_meal_request(**{"nutritional_constraints": {
        "min_calories": 1500,
        "max_calories": 2700,
        "min_protein": 9999
    }})

    response = forktimize_client.post("/meal-plan", json=meal_planner_request)

    assert response.status_code == 422
    assert response.json() == {
        "code": "macro_calories_conflict",
        "message": "Total min macro calories exceed min_calories."
    }
