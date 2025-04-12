from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine, StaticPool
from sqlmodel import select, SQLModel, Session

from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy
from jobs.collect_food_data_job import CollectFoodDataJob
from model.food import Food
from food_vendors.food_vendor import FoodVendor
from model.job_run import JobRun, JobStatus
from test.conftest import make_food

# TODO refact this test more
@pytest.fixture(scope="function")
def session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def strategy():
    strategy = MagicMock()
    strategy.fetch_foods_for.return_value = [make_food()]
    strategy.get_name.return_value = FoodVendor.CITY_FOOD
    strategy.get_raw_data.return_value = {"bombardino": "crocodilo"}

    yield strategy

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


@patch("jobs.collect_food_data_job.save_to_json")
def test_run_saves_all_foods_to_database(_, session, dummy_strategies):
    CollectFoodDataJob(session, dummy_strategies, 2, 0, fetch_images=False).run()

    food_entries = session.exec(select(Food)).all()
    assert len(food_entries) == 5, "No food entries were inserted into the database!"


@patch("jobs.collect_food_data_job.save_to_json")
def test_run_saves_raw_data_to_file(mock_save_to_json, session, dummy_strategies):
    CollectFoodDataJob(session, dummy_strategies, 2, 0, fetch_images=False).run()
    mock_save_to_json.assert_called()
    assert mock_save_to_json.call_count == 4


@patch("jobs.collect_food_data_job.save_to_json")
@freeze_time("2025-01-01")
def test_run_creates_job_run_entries_for_each_week_and_vendor(_, session, dummy_strategies):
    CollectFoodDataJob(session, dummy_strategies, 2, 0, fetch_images=False).run()

    expected = {
        (FoodVendor.CITY_FOOD, 1),
        (FoodVendor.CITY_FOOD, 2),
        (FoodVendor.INTER_FOOD, 1),
        (FoodVendor.INTER_FOOD, 2),
    }

    job_runs = session.exec(select(JobRun)).all()
    actual = {(j.food_vendor, j.week) for j in job_runs}

    assert actual == expected


def test_run_marks_job_run_as_failed_on_fetch_exception(session, strategy):
    strategy.fetch_foods_for.side_effect = Exception("Failed to fetch food data!")

    CollectFoodDataJob(session, [strategy], 2, 0, fetch_images=False).run()

    job_run = session.exec(select(JobRun)).first()
    assert job_run.status == JobStatus.FAILURE, "JobRun with FAILURE not found!"
    assert job_run.food_vendor == FoodVendor.CITY_FOOD


def test_run_creates_image_and_data_dirs_when_not_exist(session, dummy_strategies):
    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        image_dir = tmp_path / "images"
        data_dir = tmp_path / "data"

        job = CollectFoodDataJob(
            session=MagicMock(spec=Session),
            strategies=dummy_strategies,
            image_dir=image_dir,
            data_dir=data_dir,
            fetch_images=False,
            delay=0
        )

        assert not image_dir.exists()
        assert not data_dir.exists()

        job.run()

        assert image_dir.exists() and image_dir.is_dir()
        assert data_dir.exists() and data_dir.is_dir()


def test_run_downloads_and_saves_images_if_enabled(session, strategy):
    expected_img_url = "https://ca.cityfood.hu/api/v1/i?menu_item_id=1&width=425&height=425"

    strategy.fetch_foods_for.return_value = [make_food(food_id=1)]
    strategy.get_food_image_url.return_value = expected_img_url

    with TemporaryDirectory() as tmp_dir:
        image_dir = Path(tmp_dir) / "images"
        image_dir.mkdir()
        fake_image = b"image-bytes"

        job = CollectFoodDataJob(
            session=MagicMock(spec=Session),
            strategies=[strategy],
            image_dir=image_dir,
            data_dir=Path(tmp_dir) / "data",
            fetch_images=True,
            delay=0
        )

        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.content = fake_image
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            job.run()

            mock_get.assert_called_once_with(expected_img_url, timeout=10)
            image = image_dir / f"{FoodVendor.CITY_FOOD.value}_1.png"
            assert image.exists()
            assert image.read_bytes() == fake_image
