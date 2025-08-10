import logging
import time
from datetime import datetime
from pathlib import Path

import requests
from sqlmodel import Session
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log

from database.data_access import has_successful_job_run, save_foods_to_db
from database.db import ENGINE, init_db
from food_vendors.food_vendor import VENDOR_REGISTRY
from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.food_collection_strategy import FoodCollectionStrategy
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from jobs.base_job import BaseJob
from jobs.file_utils import save_to_json, save_image_to_webp
from model.food import Food
from model.job_run import JobType, FoodDataCollectorDetails
import logging

from monitoring.logging import APP_LOGGER, JOB_LOGGER
from monitoring.performance import benchmark
from settings import SETTINGS, RunMode


@benchmark
def run_collect_food_data_job(mode: RunMode = SETTINGS.MODE):
    APP_LOGGER.info(f"🔄 Running scheduled food data fetch job in {mode} mode...")
    with Session(ENGINE) as session:
        if mode == RunMode.PRODUCTION or mode == RunMode.DEVELOPMENT:
            FoodDataCollector(session, [v.strategy for v in VENDOR_REGISTRY.values()]).run()
        if mode == RunMode.TESTING:
            FoodDataCollector(session, [VENDOR_REGISTRY[FoodVendorType.CITY_FOOD].strategy]).run()


class FoodDataCollectorJob(BaseJob):
    """Individual job that collects food data for one vendor and one week."""
    
    def __init__(self,
                 session: Session,
                 strategy: FoodCollectionStrategy,
                 year: int,
                 week: int,
                 delay: float = SETTINGS.FETCHING_DELAY,
                 timeout: int = SETTINGS.FETCHING_TIMEOUT,
                 headers: dict[str, str] = SETTINGS.HEADERS,
                 fetch_images: bool = SETTINGS.FETCH_IMAGES,
                 image_dir: Path = SETTINGS.food_image_dir,
                 data_dir: Path = SETTINGS.data_dir):
        super().__init__(session, JobType.FOOD_DATA_COLLECTION)
        self._strategy = strategy
        self._year = year
        self._week = week
        self._delay = delay
        self._timeout = timeout
        self._fetch_images = fetch_images
        self._image_dir = image_dir
        self._data_dir = data_dir
        self._headers = headers

    def _create_logger_context(self) -> dict:
        """Provide vendor, week, and year context for logging."""
        return {
            "vendor": self._strategy.get_vendor().value,
            "week": self._week,
            "year": self._year
        }

    def _execute(self) -> dict:
        """Execute the job-specific work for this vendor/week combination."""
        self._sync_one_week_food_data()
        
        # Return details for job tracking using proper model
        details = FoodDataCollectorDetails(
            food_vendor=self._strategy.get_vendor(),
            week=self._week,
            year=self._year
        )
        return details.model_dump()

    def _get_failure_context(self) -> dict:
        """Provide vendor and week context for job failures."""
        return {
            "food_vendor": self._strategy.get_vendor().value,
            "week": self._week,
            "year": self._year
        }

    def _sync_one_week_food_data(self):
        # Inject contextual logger into strategy
        self._strategy.set_logger(self._logger)
        result = self._strategy.fetch_foods_for(self._year, self._week)

        self._save_raw_data_to_json(result.vendor.value, result.raw_data)
        self._save_foods_to_db(result.foods)

        if self._fetch_images:
            self._download_food_images(result.images, result.vendor.value)

    def _save_foods_to_db(self, foods: list[Food]):
        save_foods_to_db(self._session, foods)
        self._logger.info(f"✅ Food selection stored in the database")

    def _save_raw_data_to_json(self, vendor_name: str, data: dict):
        filename = self._data_dir / f"{vendor_name}-week-{self._year}-{self._week}.json"
        save_to_json(data, filename)
        self._logger.info(f"✅ Data saved to {filename}")


    def _download_food_images(self, images: dict[int, str], vendor_name: str):
        for food_id, image_url in images.items():
            image_path = self._image_dir / f"{vendor_name}_{food_id}.webp"

            if image_path.exists():
                self._logger.info(f"🟡 Skipping image (already exists): {image_path}")
                continue
            try:
                self._download_image(image_url, image_path)
                time.sleep(self._delay)
            except Exception as e:
                self._logger.warning(f"❌ Failed to download image from {image_url}: {e}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1),
        before_sleep=before_sleep_log(JOB_LOGGER, logging.WARNING),
        reraise=True
    )
    def _download_image(self, url: str, image_path: Path):
        self._logger.info(f"⬇️ Downloading image: {url}")
        response = requests.get(url, timeout=self._timeout, headers=self._headers)
        response.raise_for_status()

        save_image_to_webp(response.content, image_path)
        self._logger.info(f"✅ Saved image: {image_path}")

        return response.content


class FoodDataCollector:
    """Service that orchestrates food data collection by creating individual jobs for each vendor/week combination."""
    
    def __init__(self,
                 session: Session,
                 strategies: list[FoodCollectionStrategy],
                 logger: logging.Logger = JOB_LOGGER,
                 weeks_to_fetch: int = SETTINGS.WEEKS_TO_FETCH,
                 delay: float = SETTINGS.FETCHING_DELAY,
                 timeout: int = SETTINGS.FETCHING_TIMEOUT,
                 headers: dict[str, str] = SETTINGS.HEADERS,
                 fetch_images: bool = SETTINGS.FETCH_IMAGES,
                 image_dir: Path = SETTINGS.food_image_dir,
                 data_dir: Path = SETTINGS.data_dir):
        self._session: Session = session
        self._strategies: list[FoodCollectionStrategy] = strategies
        self._logger = logger
        self._weeks_to_fetch: int = weeks_to_fetch
        self._delay: float = delay
        self._timeout: int = timeout
        self._fetch_images: bool = fetch_images
        self._image_dir: Path = image_dir
        self._data_dir: Path = data_dir
        self._headers: dict[str, str] = headers

    def run(self):
        """Run food data collection by creating individual jobs for each vendor/week combination."""
        self._ensure_dirs_exist()
        current_year = datetime.now().year
        current_week = datetime.now().isocalendar()[1]

        for strategy in self._strategies:
            for week in range(current_week, current_week + self._weeks_to_fetch):
                if has_successful_job_run(self._session, current_year, week, strategy.get_vendor()):
                    self._logger.info(
                        f"Skipping job run for {strategy.get_vendor().value}, year:{current_year} week {week}...")
                    continue
                
                # Create and run an individual job for this vendor/week combination
                job = FoodDataCollectorJob(
                    session=self._session,
                    strategy=strategy,
                    year=current_year,
                    week=week,
                    delay=self._delay,
                    timeout=self._timeout,
                    headers=self._headers,
                    fetch_images=self._fetch_images,
                    image_dir=self._image_dir,
                    data_dir=self._data_dir
                )
                
                try:
                    job.run()
                except Exception as e:
                    self._logger.error(f"Individual job failed for {strategy.get_vendor().value} week {week}: {e}")
                    # Job already tracked its own failure, so we continue with other jobs
                
                time.sleep(self._delay)

    def _ensure_dirs_exist(self):
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._image_dir.mkdir(parents=True, exist_ok=True)



if __name__ == "__main__":
    SETTINGS.data_dir.mkdir(parents=True, exist_ok=True)
    init_db()
    client = TeletalClient("https://www.teletal.hu/etlap", "https://www.teletal.hu/ajax")
    with Session(ENGINE) as job_session:
        FoodDataCollector(job_session, [vendor.strategy for vendor in VENDOR_REGISTRY.values()], weeks_to_fetch=3).run()
