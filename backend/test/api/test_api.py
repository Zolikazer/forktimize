from datetime import date
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine, StaticPool
from sqlmodel import SQLModel, Session
from starlette.testclient import TestClient

from database.db import get_session
from main import app
from model.food import Food
from routers.planner_routes import AppStatus


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
    food_items = [
        Food(food_id=1, name="Grilled Chicken", calories=500, protein=50, carb=20, fat=10, price=1000,
             date=date(2025, 2, 24)),
        Food(food_id=2, name="Salmon", calories=600, protein=55, carb=10, fat=25, price=1200, date=date(2025, 2, 24)),
        Food(food_id=3, name="Lencsefőzelék vagdalttal", calories=400, protein=20, carb=50, fat=10, price=800,
             date=date(2025, 2, 24)),
        Food(food_id=4, name="Steak", calories=800, protein=70, carb=5, fat=40, price=2000, date=date(2025, 2, 24)),
        Food(food_id=5, name="Pasta", calories=500, protein=15, carb=80, fat=5, price=800, date=date(2025, 2, 24)),
        Food(food_id=6, name="Cake", calories=500, protein=15, carb=80, fat=5, price=800, date=date(2025, 2, 25)),
        Food(food_id=6, name="Fish", calories=500, protein=15, carb=80, fat=5, price=800, date=date(2025, 2, 23)),

    ]
    session.add_all(food_items)
    session.commit()


def test_create_menu_endpoint(client, session: Session):
    insert_test_food(session)

    requested_date = "2025-02-24"
    menu_request = {
        "date": requested_date,
        "nutritional_constraints": {
            "min_calories": 1500,
            "max_calories": 2700,
            "min_protein": 200
        },
        "food_blacklist": ["Lencsefőzelék"]
    }

    response = client.post("/menu", json=menu_request)

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


def test_create_menu_max_food_repeat(client, session: Session):
    insert_test_food(session)

    requested_date = "2025-02-24"
    menu_request = {
        "date": requested_date,
        "nutritional_constraints": {
            "min_calories": 1500,
            "max_calories": 2700,
            "min_protein": 200
        },
        "food_blacklist": ["Lencsefőzelék"],
        "max_food_repeat": 1,
    }

    response = client.post("/menu", json=menu_request)

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
