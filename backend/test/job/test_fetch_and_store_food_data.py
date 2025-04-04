from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy import create_engine, StaticPool
from sqlmodel import select, SQLModel, Session

from jobs.fetch_food_selection_job import fetch_and_store_food_selection
from model.food_vendors import FoodVendor
from model.food import Food
from model.job_run import JobRun, JobStatus
from test.food_factory import make_food


@pytest.fixture(scope="function")
def test_session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_fetch_and_store_food_data_success(test_session):
    strategy = MagicMock()
    strategy.fetch_foods_for.return_value = [make_food(), make_food(), make_food()]
    strategy.get_name.return_value = FoodVendor.CITY_FOOD
    strategy.get_raw_data.return_value = {"bombardino": "crocodilo"}

    with patch("jobs.fetch_food_selection_job.save_to_json") as mock_save_to_file:
        fetch_and_store_food_selection(test_session, strategy)
        mock_save_to_file.assert_called()

        job_run = test_session.exec(select(JobRun)).first()
        assert job_run.status == JobStatus.SUCCESS, "JobRun with SUCCESS not found!"
        assert job_run.food_vendor == FoodVendor.CITY_FOOD

        food_entries = test_session.exec(select(Food)).all()
        assert len(food_entries) == 3, "No food entries were inserted into the database!"


def test_fetch_fails_and_marks_job_as_failed(test_session):
    strategy = MagicMock()
    strategy.fetch_foods_for.side_effect = Exception("Failed to fetch food data!")
    strategy.get_name.return_value = FoodVendor.CITY_FOOD

    fetch_and_store_food_selection(test_session, strategy)

    job_run = test_session.exec(select(JobRun)).first()
    assert job_run.status == JobStatus.FAILURE, "JobRun with FAILURE not found!"
    assert job_run.food_vendor == FoodVendor.CITY_FOOD
