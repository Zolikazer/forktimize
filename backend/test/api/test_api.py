from datetime import date
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine, StaticPool
from sqlmodel import SQLModel, Session
from starlette.testclient import TestClient

from database.db import get_session
from model.food_vendors import FoodVendor
from main import app
from routers.meal_planner import AppStatus
from test.food_factory import make_food


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def client(session):
    app.dependency_overrides[get_session] = lambda: session
    return TestClient(app)


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


def test_create_meal_plan_endpoint(client, session: Session):
    insert_test_food(session)
    session.add(make_food(price=0, food_vendor=FoodVendor.INTER_FOOD))

    requested_date = "2025-02-24"
    meal_plan_request = {
        "date": requested_date,
        "nutritional_constraints": {
            "min_calories": 1500,
            "max_calories": 2700,
            "min_protein": 200
        },
        "food_blacklist": ["Lencsefőzelék"],
        "food_vendor": "cityfood",
    }

    response = client.post("/meal-plan", json=meal_plan_request)

    assert response.status_code == 200
    data = response.json()

    assert data["date"] == requested_date
    assert len(data["foods"]) == 4

    food_names = [f["name"] for f in data["foods"]]
    assert "Lencsefőzelék vagdalttal" not in food_names

    food_log_entry = data["foodLogEntry"]
    assert food_log_entry["chicken"] == 800
    assert food_log_entry["oil"] == 16
    assert food_log_entry["sugar"] == 80

    assert data["totalPrice"] == 4000
    assert data["totalCalories"] == 2000
    assert data["totalProtein"] == 200
    assert data["totalCarbs"] == 80
    assert data["totalFat"] == 40
    assert data["foodVendor"] == "cityfood"


def test_create_meal_plan_max_food_repeat(client, session: Session):
    insert_test_food(session)

    requested_date = "2025-02-24"
    meal_planner_request = {
        "date": requested_date,
        "nutritional_constraints": {
            "min_calories": 1500,
            "max_calories": 2700,
            "min_protein": 200
        },
        "food_blacklist": ["Lencsefőzelék"],
        "max_food_repeat": 1,
        "food_vendor": "cityfood",
    }

    response = client.post("/meal-plan", json=meal_planner_request)

    assert response.status_code == 200
    data = response.json()

    food_names = [f["name"] for f in data["foods"]]
    name_counts = {name: food_names.count(name) for name in food_names}

    for name, count in name_counts.items():
        assert count == 1, f"Food '{name}' appears {count} times"


@freeze_time("2025-02-23")
def test_get_available_dates(client, session):
    insert_test_food(session)

    response = client.get("/dates")

    assert response.status_code == 200
    assert response.json() == ["2025-02-24", "2025-02-25"]


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "HEALTHY", "database": "connected"}


def test_health_check_unhealthy(client):
    broken_session = MagicMock()
    broken_session.exec.side_effect = Exception("Database gone fishing 🐟")

    app.dependency_overrides = {
        get_session: lambda: broken_session
    }

    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": AppStatus.UNHEALTHY,
        "database": "error"
    }


def test_invalid_meal_plan_reqeust(client):
    requested_date = "2025-02-24"
    meal_planner_request = {
        "date": requested_date,
        "nutritional_constraints": {
            "min_calories": 1500,
            "max_calories": 2700,
            "min_protein": 9999
        },
        "food_blacklist": ["Lencsefőzelék"],
        "max_food_repeat": 1,
        "food_vendor": "cityfood",
    }

    response = client.post("/meal-plan", json=meal_planner_request)

    assert response.status_code == 422
    assert response.json() == {
        "code": "macro_calories_conflict",
        "message": "Total min macro calories exceed min_calories."
    }
