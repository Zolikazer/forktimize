from unittest.mock import patch, MagicMock

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine, StaticPool
from sqlmodel import select, SQLModel, Session

from jobs.collect_food_data_job import CollectFoodDataJob
from jobs.food_vendors_strategies.food_vendor_strategy import FoodVendorStrategy
from model.food import Food
from model.food_vendors import FoodVendor
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


@pytest.fixture(scope="function")
def dummy_strategy():
    strategy = MagicMock()
    strategy.fetch_foods_for.return_value = [make_food(), make_food(), make_food()]
    strategy.get_name.return_value = FoodVendor.CITY_FOOD
    strategy.get_raw_data.return_value = {"bombardino": "crocodilo"}


@pytest.fixture
def dummy_strategies() -> list[FoodVendorStrategy]:
    def make_strategy(vendor_name: FoodVendor, foods: list[Food]) -> FoodVendorStrategy:
        strategy = MagicMock(spec=FoodVendorStrategy)
        strategy.get_name.return_value = vendor_name
        strategy.fetch_foods_for.return_value = foods
        strategy.get_raw_data.return_value = {"something": "something"}

        return strategy

    return [
        make_strategy(FoodVendor.CITY_FOOD, [make_food(), make_food(), make_food()]),
        make_strategy(FoodVendor.INTER_FOOD, [make_food(), make_food()]),
    ]


@patch("jobs.collect_food_data_job.save_to_json", autospec=True)
def test_collect_food_data_saves_foods_to_db(_, test_session, dummy_strategies):
    CollectFoodDataJob(test_session, dummy_strategies, 2, 0).run()

    food_entries = test_session.exec(select(Food)).all()
    assert len(food_entries) == 5, "No food entries were inserted into the database!"


def test_collect_food_data_saves_data(test_session, dummy_strategies):
    with patch("jobs.collect_food_data_job.save_to_json") as mock_save_to_file:
        CollectFoodDataJob(test_session, dummy_strategies, 2, 0).run()
        mock_save_to_file.assert_called()
        assert mock_save_to_file.call_count == 4


@patch("jobs.collect_food_data_job.save_to_json", autospec=True)
@freeze_time("2025-01-01")
def test_collect_food_data_track_successful_job_runs(_, test_session, dummy_strategies):
    CollectFoodDataJob(test_session, dummy_strategies, 2, 0).run()

    expected = {
        (FoodVendor.CITY_FOOD, 1),
        (FoodVendor.CITY_FOOD, 2),
        (FoodVendor.INTER_FOOD, 1),
        (FoodVendor.INTER_FOOD, 2),
    }

    job_runs = test_session.exec(select(JobRun)).all()
    actual = {(j.food_vendor, j.week) for j in job_runs}

    assert actual == expected


def test_fetch_fails_and_marks_job_as_failed(test_session):
    strategy = MagicMock()
    strategy.fetch_foods_for.side_effect = Exception("Failed to fetch food data!")
    strategy.get_name.return_value = FoodVendor.CITY_FOOD
    CollectFoodDataJob(test_session, [strategy], 2, 0).run()

    job_run = test_session.exec(select(JobRun)).first()
    assert job_run.status == JobStatus.FAILURE, "JobRun with FAILURE not found!"
    assert job_run.food_vendor == FoodVendor.CITY_FOOD
