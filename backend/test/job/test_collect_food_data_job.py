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
    strategy.fetch_foods_for.return_value = [make_food()]
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
    CollectFoodDataJob(test_session, dummy_strategies, 2, 0, fetch_images=False).run()

    food_entries = test_session.exec(select(Food)).all()
    assert len(food_entries) == 5, "No food entries were inserted into the database!"


def test_collect_food_data_saves_data(test_session, dummy_strategies):
    with patch("jobs.collect_food_data_job.save_to_json") as mock_save_to_file:
        CollectFoodDataJob(test_session, dummy_strategies, 2, 0, fetch_images=False).run()
        mock_save_to_file.assert_called()
        assert mock_save_to_file.call_count == 4


@patch("jobs.collect_food_data_job.save_to_json", autospec=True)
@freeze_time("2025-01-01")
def test_collect_food_data_track_successful_job_runs(_, test_session, dummy_strategies):
    CollectFoodDataJob(test_session, dummy_strategies, 2, 0, fetch_images=False).run()

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
    CollectFoodDataJob(test_session, [strategy], 2, 0, fetch_images=False).run()

    job_run = test_session.exec(select(JobRun)).first()
    assert job_run.status == JobStatus.FAILURE, "JobRun with FAILURE not found!"
    assert job_run.food_vendor == FoodVendor.CITY_FOOD


def test_collect_food_data_creates_necessary_directory(test_session, dummy_strategies):
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


def test_collect_food_data_fetches_images(test_session):
    expected_img_url = "https://ca.cityfood.hu/api/v1/i?menu_item_id=1&width=425&height=425"

    strategy = MagicMock()
    strategy.fetch_foods_for.return_value = [make_food(food_id=1)]
    strategy.get_name.return_value = FoodVendor.CITY_FOOD
    strategy.get_raw_data.return_value = {"bombardino": "crocodilo"}
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
