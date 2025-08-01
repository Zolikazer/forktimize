from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock, call

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine
from sqlmodel import select, SQLModel, Session

from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.food_collection_strategy import FoodCollectionStrategy, StrategyResult
from jobs.food_data_collector_job import FoodDataCollector, FoodDataCollectorJob
from model.food import Food
from model.job_run import JobRun, JobStatus
from settings import SETTINGS
from test.conftest import make_food


# Fixtures
@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def strategy():
    food = make_food()
    strategy = MagicMock(spec=FoodCollectionStrategy)
    strategy.fetch_foods_for.return_value = StrategyResult(foods=[food],
                                                           raw_data={"bombardino": "crocodilo"},
                                                           images={food.food_id: "sometething"},
                                                           vendor=FoodVendorType.CITY_FOOD)
    strategy.get_vendor.return_value = FoodVendorType.CITY_FOOD
    return strategy


@pytest.fixture
def strategies() -> list[FoodCollectionStrategy]:
    def make_strategy(vendor: FoodVendorType, foods: list[Food]) -> FoodCollectionStrategy:
        strategy = MagicMock(spec=FoodCollectionStrategy)
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


# =============================================================================
# FoodDataCollector Tests (Orchestration Logic)
# =============================================================================

@patch("jobs.food_data_collector_job.FoodDataCollectorJob", autospec=True)
@freeze_time("2025-01-01")
def test_collector_creates_jobs_for_each_vendor_week_combination(mock_job_class, session, strategies):
    """Test that collector creates individual jobs for each vendor/week combination."""
    mock_job_instance = MagicMock()
    mock_job_class.return_value = mock_job_instance
    
    collector = FoodDataCollector(session, strategies, weeks_to_fetch=2, delay=0)
    collector.run()
    
    # Should create 4 jobs: 2 vendors × 2 weeks
    assert mock_job_class.call_count == 4
    assert mock_job_instance.run.call_count == 4
    
    # Verify correct number of job creation calls with correct parameters
    calls = mock_job_class.call_args_list
    assert len(calls) == 4
    
    # Check that jobs were created for both strategies and both weeks
    vendors = [call.kwargs['strategy'].get_vendor() for call in calls]
    weeks = [call.kwargs['week'] for call in calls]
    
    assert vendors.count(FoodVendorType.CITY_FOOD) == 2
    assert vendors.count(FoodVendorType.INTER_FOOD) == 2
    assert weeks.count(1) == 2  # Both vendors for week 1
    assert weeks.count(2) == 2  # Both vendors for week 2


@patch("jobs.food_data_collector_job.FoodDataCollectorJob", autospec=True)
@patch("jobs.food_data_collector_job.has_successful_job_run")
@freeze_time("2025-01-01") 
def test_collector_skips_jobs_with_successful_runs(mock_has_successful, mock_job_class, session, strategy):
    """Test that collector skips creating jobs for vendor/week combinations that already succeeded."""
    mock_has_successful.return_value = True
    mock_job_instance = MagicMock()
    mock_job_class.return_value = mock_job_instance
    
    collector = FoodDataCollector(session, [strategy], weeks_to_fetch=2, delay=0)
    collector.run()
    
    # Should not create any jobs since all are successful
    mock_job_class.assert_not_called()
    mock_job_instance.run.assert_not_called()
    
    # Should check for successful runs
    assert mock_has_successful.call_count == 2


@patch("jobs.food_data_collector_job.FoodDataCollectorJob", autospec=True)
def test_collector_continues_after_individual_job_failure(mock_job_class, session, strategies):
    """Test that collector continues processing other jobs when one fails."""
    mock_job_instance = MagicMock()
    mock_job_class.return_value = mock_job_instance
    
    # Make the first job fail, others succeed
    mock_job_instance.run.side_effect = [Exception("Job failed!"), None, None, None]
    
    collector = FoodDataCollector(session, strategies, weeks_to_fetch=2, delay=0)
    collector.run()  # Should not raise exception
    
    # Should still create and run all 4 jobs
    assert mock_job_class.call_count == 4
    assert mock_job_instance.run.call_count == 4


def test_collector_creates_directories(session, strategies):
    """Test that collector creates necessary directories."""
    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        image_dir = tmp_path / "images"
        data_dir = tmp_path / "data"

        with patch("jobs.food_data_collector_job.FoodDataCollectorJob", autospec=True):
            collector = FoodDataCollector(
                session=session,
                strategies=strategies,
                image_dir=image_dir,
                data_dir=data_dir,
                weeks_to_fetch=1,
                delay=0
            )

            assert not image_dir.exists()
            assert not data_dir.exists()

            collector.run()

            assert image_dir.exists() and image_dir.is_dir()
            assert data_dir.exists() and data_dir.is_dir()


@patch("jobs.food_data_collector_job.FoodDataCollectorJob", autospec=True)
@patch("time.sleep")
def test_collector_respects_delay_between_jobs(mock_sleep, mock_job_class, session, strategies):
    """Test that collector waits specified delay between jobs."""
    mock_job_instance = MagicMock()
    mock_job_class.return_value = mock_job_instance
    
    delay = 1.5
    collector = FoodDataCollector(session, strategies, weeks_to_fetch=1, delay=delay)
    collector.run()
    
    # Should sleep after each job (2 jobs total)
    assert mock_sleep.call_count == 2
    mock_sleep.assert_has_calls([call(delay), call(delay)])


# =============================================================================
# FoodDataCollectorJob Tests (Individual Job Logic)
# =============================================================================

@freeze_time("2025-01-01")
def test_individual_job_handles_single_vendor_week(session, strategy):
    """Test that individual job handles a single vendor/week combination correctly."""
    year = 2025
    week = 1
    
    job = FoodDataCollectorJob(
        session=session,
        strategy=strategy,
        year=year,
        week=week,
        delay=0,
        fetch_images=False,
        data_dir=Path("/tmp/data"),
        image_dir=Path("/tmp/images")
    )
    
    with patch("jobs.food_data_collector_job.save_to_json"):
        job.run()
    
    # Should create exactly one job run
    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 1
    
    job_run = job_runs[0]
    assert job_run.status == JobStatus.SUCCESS
    assert job_run.details['food_vendor'] == FoodVendorType.CITY_FOOD.value
    assert job_run.details['week'] == week
    assert job_run.details['year'] == year


def test_individual_job_tracks_failure_correctly(session, strategy):
    """Test that individual job tracks failures correctly."""
    strategy.fetch_foods_for.side_effect = Exception("Network error!")
    
    job = FoodDataCollectorJob(
        session=session,
        strategy=strategy,
        year=2025,
        week=1,
        delay=0,
        fetch_images=False,
        data_dir=Path("/tmp/data"),
        image_dir=Path("/tmp/images")
    )
    
    with pytest.raises(Exception, match="Network error!"):
        job.run()
    
    # Should create exactly one failed job run
    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 1
    
    job_run = job_runs[0]
    assert job_run.status == JobStatus.FAILURE
    # BaseJob now stores error message plus job-specific context for failures
    assert job_run.details['error'] == "Network error!"
    assert job_run.details['food_vendor'] == FoodVendorType.CITY_FOOD.value
    assert job_run.details['week'] == 1
    assert job_run.details['year'] == 2025


@patch("jobs.food_data_collector_job.save_to_json")
def test_individual_job_saves_foods_to_database(mock_save_json, session, strategy):
    """Test that individual job saves foods to database."""
    foods = [make_food(), make_food()]
    strategy.fetch_foods_for.return_value = StrategyResult(
        foods=foods, raw_data={}, images={}, vendor=FoodVendorType.CITY_FOOD
    )
    
    job = FoodDataCollectorJob(
        session=session, strategy=strategy, year=2025, week=1,
        delay=0, fetch_images=False, data_dir=Path("/tmp"), image_dir=Path("/tmp")
    )
    job.run()
    
    # Check foods were saved
    saved_foods = session.exec(select(Food)).all()
    assert len(saved_foods) == 2


@patch("jobs.food_data_collector_job.save_to_json")
def test_individual_job_saves_raw_data_to_json(mock_save_json, session, strategy):
    """Test that individual job saves raw data as JSON."""
    raw_data = {"menu": "pizza", "items": [1, 2, 3]}
    strategy.fetch_foods_for.return_value = StrategyResult(
        foods=[], raw_data=raw_data, images={}, vendor=FoodVendorType.CITY_FOOD
    )
    
    job = FoodDataCollectorJob(
        session=session, strategy=strategy, year=2025, week=42,
        delay=0, fetch_images=False, data_dir=Path("/tmp/data"), image_dir=Path("/tmp")
    )
    job.run()
    
    # Check JSON was saved with correct filename
    expected_filename = Path("/tmp/data/cityfood-week-2025-42.json")
    mock_save_json.assert_called_once_with(raw_data, expected_filename)


@patch("jobs.food_data_collector_job.save_to_json")
@patch("jobs.food_data_collector_job.save_image_to_webp")
def test_individual_job_downloads_images_when_enabled(mock_save_image, mock_save_json, session, strategy):
    """Test that individual job downloads images when fetch_images=True."""
    image_url = "https://example.com/food.jpg"
    images = {123: image_url}
    strategy.fetch_foods_for.return_value = StrategyResult(
        foods=[], raw_data={}, images=images, vendor=FoodVendorType.CITY_FOOD
    )
    
    fake_image_content = b"fake-image-bytes"
    image_dir = Path("/tmp/images")
    
    job = FoodDataCollectorJob(
        session=session, strategy=strategy, year=2025, week=1,
        delay=0, fetch_images=True, data_dir=Path("/tmp"), image_dir=image_dir
    )
    
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.content = fake_image_content
        mock_get.return_value = mock_response
        
        job.run()
        
        # Check image was downloaded and saved
        mock_get.assert_called_once_with(image_url, timeout=30, headers=SETTINGS.HEADERS)
        expected_image_path = image_dir / "cityfood_123.webp"
        mock_save_image.assert_called_once_with(fake_image_content, expected_image_path)


@patch("jobs.food_data_collector_job.save_to_json")
def test_individual_job_skips_images_when_disabled(mock_save_json, session, strategy):
    """Test that individual job skips image download when fetch_images=False."""
    images = {123: "https://example.com/food.jpg"}
    strategy.fetch_foods_for.return_value = StrategyResult(
        foods=[], raw_data={}, images=images, vendor=FoodVendorType.CITY_FOOD
    )
    
    job = FoodDataCollectorJob(
        session=session, strategy=strategy, year=2025, week=1,
        delay=0, fetch_images=False, data_dir=Path("/tmp"), image_dir=Path("/tmp")
    )
    
    with patch("requests.get") as mock_get:
        job.run()
        
        # Should not download any images
        mock_get.assert_not_called()


@patch("jobs.food_data_collector_job.save_to_json")
@patch("jobs.food_data_collector_job.save_image_to_webp")
def test_individual_job_skips_existing_images(mock_save_image, mock_save_json, session, strategy):
    """Test that individual job skips downloading images that already exist."""
    images = {123: "https://example.com/food.jpg"}
    strategy.fetch_foods_for.return_value = StrategyResult(
        foods=[], raw_data={}, images=images, vendor=FoodVendorType.CITY_FOOD
    )
    
    with TemporaryDirectory() as tmp_dir:
        image_dir = Path(tmp_dir)
        existing_image = image_dir / "cityfood_123.webp"
        existing_image.touch()  # Create the file
        
        job = FoodDataCollectorJob(
            session=session, strategy=strategy, year=2025, week=1,
            delay=0, fetch_images=True, data_dir=Path("/tmp"), image_dir=image_dir
        )
        
        with patch("requests.get") as mock_get:
            job.run()
            
            # Should not download since image exists
            mock_get.assert_not_called()
            mock_save_image.assert_not_called()


@patch("jobs.food_data_collector_job.save_to_json")
@patch("jobs.food_data_collector_job.save_image_to_webp")
def test_individual_job_continues_on_image_download_failure(mock_save_image, mock_save_json, session, strategy):
    """Test that individual job continues even if image download fails."""
    images = {123: "https://example.com/food.jpg", 456: "https://example.com/food2.jpg"}
    strategy.fetch_foods_for.return_value = StrategyResult(
        foods=[], raw_data={}, images=images, vendor=FoodVendorType.CITY_FOOD
    )
    
    job = FoodDataCollectorJob(
        session=session, strategy=strategy, year=2025, week=1,
        delay=0, fetch_images=True, data_dir=Path("/tmp"), image_dir=Path("/tmp")
    )
    
    # Mock the _download_image method directly to avoid retry complexity
    with patch.object(job, '_download_image') as mock_download:
        mock_download.side_effect = [Exception("Network error"), None]  # First fails, second succeeds
        
        job.run()  # Should not raise exception
        
        # Should have tried both images
        assert mock_download.call_count == 2


@patch("jobs.food_data_collector_job.save_to_json")
@patch("jobs.food_data_collector_job.save_image_to_webp")
@patch("time.sleep")
def test_individual_job_respects_delay_between_image_downloads(mock_sleep, mock_save_image, mock_save_json, session, strategy):
    """Test that individual job waits between image downloads."""
    images = {123: "https://example.com/1.jpg", 456: "https://example.com/2.jpg"}
    strategy.fetch_foods_for.return_value = StrategyResult(
        foods=[], raw_data={}, images=images, vendor=FoodVendorType.CITY_FOOD
    )
    
    delay = 0.5
    job = FoodDataCollectorJob(
        session=session, strategy=strategy, year=2025, week=1,
        delay=delay, fetch_images=True, data_dir=Path("/tmp"), image_dir=Path("/tmp")
    )
    
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(content=b"image")
        
        job.run()
        
        # Should sleep after each image download
        assert mock_sleep.call_count == 2
        mock_sleep.assert_has_calls([call(delay), call(delay)])
