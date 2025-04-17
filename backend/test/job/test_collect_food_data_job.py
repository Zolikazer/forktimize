from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine, StaticPool
from sqlmodel import select, SQLModel, Session

from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy, StrategyResult
from jobs.food_data_collector_job import FoodDataCollectorJob
from model.food import Food
from model.job_run import JobRun, JobStatus
from settings import SETTINGS
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
    food = make_food()
    strategy = MagicMock()
    strategy.fetch_foods_for.return_value = StrategyResult(foods=[food],
                                                           raw_data={"bombardino": "crocodilo"},
                                                           images={food.food_id: "sometething"},
                                                           vendor=FoodVendorType.CITY_FOOD)
    strategy.get_vendor.return_value = FoodVendorType.CITY_FOOD

    yield strategy


@pytest.fixture
def strategies() -> list[FoodVendorStrategy]:
    def make_strategy(vendor: FoodVendorType, foods: list[Food]) -> FoodVendorStrategy:
        strategy = MagicMock(spec=FoodVendorStrategy)
        strategy.get_vendor.return_value = vendor
        strategy.fetch_foods_for.return_value = StrategyResult(foods=foods,
                                                               raw_data={"bombardino": "crocodilo"},
                                                               images={f.food_id: "sometething" for f in foods},
                                                               vendor=vendor)

        return strategy

    return [
        make_strategy(FoodVendorType.CITY_FOOD, [make_food(), make_food(), make_food()]),
        make_strategy(FoodVendorType.INTER_FOOD, [make_food(), make_food()]),
    ]


@patch("jobs.food_data_collector_job.save_to_json")
def test_run_saves_all_foods_to_database(_, session, strategies):
    FoodDataCollectorJob(session, strategies, 2, 0, fetch_images=False).run()

    food_entries = session.exec(select(Food)).all()
    assert len(food_entries) == 5, "No food entries were inserted into the database!"


@patch("jobs.food_data_collector_job.save_to_json")
def test_run_saves_raw_data_to_file(mock_save_to_json, session, strategies):
    FoodDataCollectorJob(session, strategies, 2, 0, fetch_images=False).run()
    mock_save_to_json.assert_called()
    assert mock_save_to_json.call_count == 4


@patch("jobs.food_data_collector_job.save_to_json")
@freeze_time("2025-01-01")
def test_run_creates_job_run_entries_for_each_week_and_vendor(_, session, strategies):
    FoodDataCollectorJob(session, strategies, 2, 0, fetch_images=False).run()

    expected = {
        (FoodVendorType.CITY_FOOD, 1),
        (FoodVendorType.CITY_FOOD, 2),
        (FoodVendorType.INTER_FOOD, 1),
        (FoodVendorType.INTER_FOOD, 2),
    }

    job_runs = session.exec(select(JobRun)).all()
    actual = {(j.food_vendor, j.week) for j in job_runs}

    assert actual == expected


def test_run_marks_job_run_as_failed_on_fetch_exception(session, strategy):
    strategy.fetch_foods_for.side_effect = Exception("Failed to fetch food data!")

    FoodDataCollectorJob(session, [strategy], 2, 0, fetch_images=False).run()

    job_run = session.exec(select(JobRun)).first()
    assert job_run.status == JobStatus.FAILURE, "JobRun with FAILURE not found!"
    assert job_run.food_vendor == FoodVendorType.CITY_FOOD


def test_run_creates_image_and_data_dirs_when_not_exist(session, strategies):
    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        image_dir = tmp_path / "images"
        data_dir = tmp_path / "data"

        job = FoodDataCollectorJob(
            session=MagicMock(spec=Session),
            strategies=strategies,
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


@pytest.mark.parametrize("image_url, expected_ext", [
    ("https://example.com/image.png", "png"),
    ("https://example.com/image.jpeg", "jpeg"),
    ("https://example.com/image.jpg", "jpg"),
    ("https://example.com/image", "png"),
])
def test_run_downloads_and_saves_images_if_enabled(session, strategy, image_url, expected_ext):
    strategy.fetch_foods_for.return_value = StrategyResult(images={1: image_url},
                                                           foods=[],
                                                           raw_data={},
                                                           vendor=strategy.get_vendor())
    # TODO: mock it
    with TemporaryDirectory() as tmp_dir:
        image_dir = Path(tmp_dir) / "images"
        image_dir.mkdir()
        fake_image = b"image-bytes"

        job = FoodDataCollectorJob(
            session=session,
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

            mock_get.assert_called_once_with(image_url, timeout=30, headers=SETTINGS.HEADERS)
            image = image_dir / f"{strategy.get_vendor().value}_1.{expected_ext}"
            assert image.exists()
            assert image.read_bytes() == fake_image


@freeze_time("2025-01-01")
def test_job_skips_if_successful_run_already_exists(session, strategy):
    now = datetime.now()
    week = now.isocalendar()[1]
    year = now.year

    existing = JobRun(
        week=week,
        year=year,
        status=JobStatus.SUCCESS,
        timestamp=now,
        food_vendor=FoodVendorType.CITY_FOOD
    )
    session.add(existing)
    session.commit()

    job = FoodDataCollectorJob(session, [strategy], weeks_to_fetch=1, delay=0, fetch_images=False)
    job.run()

    assert session.exec(select(Food)).first() is None, "Expected no food to be added — job should be skipped!"

    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 1 and job_runs[0].id == existing.id, "Expected no new JobRun if already successful"
