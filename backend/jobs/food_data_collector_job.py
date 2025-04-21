import random
import time
from datetime import datetime
from pathlib import Path

import requests
from sqlmodel import Session

from database.data_access import has_successful_job_run
from database.db import ENGINE, init_db
from food_vendors.food_vendor import VENDOR_REGISTRY
from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.food_vendor_strategy import FoodCollectionStrategy
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from jobs.file_utils import save_to_json, save_image_to_webp
from model.food import Food
from model.job_run import JobStatus, JobRun
from monitoring.logging import JOB_LOGGER, APP_LOGGER
from monitoring.performance import benchmark
from settings import SETTINGS, RunMode


@benchmark
def run_collect_food_data_job(mode: RunMode = SETTINGS.MODE):
    APP_LOGGER.info(f"🔄 Running scheduled food data fetch job in {mode} mode...")
    with Session(ENGINE) as session:
        if mode == RunMode.PRODUCTION or mode == RunMode.DEVELOPMENT:
            FoodDataCollectorJob(session, [v.strategy for v in VENDOR_REGISTRY.values()]).run()
        if mode == RunMode.TESTING:
            FoodDataCollectorJob(session, [VENDOR_REGISTRY[FoodVendorType.CITY_FOOD].strategy]).run()


class FoodDataCollectorJob:
    FORKTIMIZE_HEADERS = {
        "User-Agent": "ForktimizeBot/1.0 (+https://forktimize.xyz/bot-info)",
        "From": "spagina.zoltan@gmail.com",
        "X-Forktimize-Purpose": "Meal planning helper, not scraping for resale or spam. Contact: forktimize.xyz"
    }

    def __init__(self,
                 session: Session,
                 strategies: list[FoodCollectionStrategy],
                 weeks_to_fetch: int = SETTINGS.WEEKS_TO_FETCH,
                 delay: float = SETTINGS.FETCHING_DELAY,
                 timeout: int = SETTINGS.FETCHING_TIMEOUT,
                 headers: dict[str, str] = SETTINGS.HEADERS,
                 fetch_images: bool = SETTINGS.FETCH_IMAGES,
                 image_dir: Path = SETTINGS.food_image_dir,
                 data_dir: Path = SETTINGS.data_dir):
        self._session: Session = session
        self._strategies: list[FoodCollectionStrategy] = strategies
        self._weeks_to_fetch: int = weeks_to_fetch
        self._delay: float = delay
        self._timeout: int = timeout
        self._fetch_images: bool = fetch_images
        self._image_dir: Path = image_dir
        self._data_dir: Path = data_dir
        self._headers: dict[str, str] = headers

    def run(self):
        self._ensure_dirs_exist()
        current_year = datetime.now().year
        current_week = datetime.now().isocalendar()[1]

        for strategy in self._strategies:
            for week in range(current_week, current_week + self._weeks_to_fetch):
                if has_successful_job_run(self._session, current_year, week, strategy.get_vendor()):
                    JOB_LOGGER.info(
                        f"Skipping job run for {strategy.get_vendor().value}, year:{current_year} week {week}...")
                    continue
                try:
                    self._sync_one_week_food_data(current_year, week, strategy)
                    self._track_successful_job_run(current_year, strategy.get_vendor(), week)
                except Exception as e:
                    self._track_failed_job_run(current_year, e, strategy.get_vendor(), week)

                time.sleep(self._delay)

    def _ensure_dirs_exist(self):
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._image_dir.mkdir(parents=True, exist_ok=True)

    def _sync_one_week_food_data(self, year: int, week: int, strategy: FoodCollectionStrategy):
        result = strategy.fetch_foods_for(year, week)

        self._save_foods_to_json(result.vendor.value, result.raw_data, year, week)
        self._save_food_to_db(result.foods, week)

        if self._fetch_images:
            self._download_food_images(result.images, result.vendor.value)

    def _save_food_to_db(self, foods: list[Food], week: int):
        self._session.add_all(foods)
        self._session.commit()

        JOB_LOGGER.info(f"✅ Week {week} food selection stored in the database.")

    def _save_foods_to_json(self, vendor_name: str, data: dict, year: int, week: int):
        filename = self._data_dir / f"{vendor_name}-week-{year}-{week}.json"
        save_to_json(data, filename)

        JOB_LOGGER.info(f"✅ Week {week} data saved to {filename}.")

    def _track_successful_job_run(self, current_year: int, vendor: FoodVendorType, week: int):
        job_id = self._track_job_run(week, current_year, JobStatus.SUCCESS, vendor)
        JOB_LOGGER.info(
            f"✅ Job ID={job_id}: Successfully fetched & stored data for {vendor.value} Week {week}.")

    def _track_job_run(self, week: int, year: int, status: JobStatus, vendor: FoodVendorType) -> int:
        job_run = JobRun(week=week, year=year, status=status, timestamp=datetime.now(), food_vendor=vendor)
        self._session.add(job_run)
        self._session.commit()
        self._session.refresh(job_run)

        JOB_LOGGER.info(f"📌 Job Run Logged: ID={job_run.id}, Week={week}, Year={year}, Status={status}")
        return job_run.id

    def _track_failed_job_run(self, current_year: int, e: Exception, vendor: FoodVendorType, week: int):
        job_id = self._track_job_run(week, current_year, JobStatus.FAILURE, vendor)
        JOB_LOGGER.error(f"❌ Job ID={job_id}: Unexpected error: {e}")

    def _download_food_images(self, images: dict[int, str], vendor_name: str):
        for food_id, image in images.items():
            image_path = self._image_dir / f"{vendor_name}_{food_id}.webp"

            if image_path.exists():
                JOB_LOGGER.info(f"🟡 Skipping image (already exists): {image_path}")
                continue

            self._download_image(image, image_path)
            time.sleep(self._delay + random.uniform(0.1, 0.5))

    def _download_image(self, url: str, image_path: Path):
        JOB_LOGGER.info(f"⬇️ Downloading image: {url}")
        try:
            response = requests.get(url, timeout=self._timeout, headers=self._headers)
            response.raise_for_status()

            save_image_to_webp(response.content, image_path)
            JOB_LOGGER.info(f"✅ Saved image: {image_path}")

            return response.content
        except Exception as e:
            JOB_LOGGER.warning(f"❌ Failed to download image from {url}: {e}")

        return None


if __name__ == "__main__":
    SETTINGS.data_dir.mkdir(parents=True, exist_ok=True)
    init_db()
    client = TeletalClient("https://www.teletal.hu/etlap", "https://www.teletal.hu/ajax")
    with Session(ENGINE) as job_session:
        FoodDataCollectorJob(job_session, [vendor.strategy for vendor in VENDOR_REGISTRY.values()], 2).run()
