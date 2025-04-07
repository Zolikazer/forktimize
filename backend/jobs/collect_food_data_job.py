import time
from datetime import datetime
from pathlib import Path

import requests
from sqlmodel import Session

from database.db import init_db, engine
from jobs.food_vendors_strategies.food_vendor_strategy import FoodVendorStrategy
from jobs.food_vendors_strategies.vendor_strategies import VENDOR_STRATEGIES
from jobs.serialization import save_to_json
from model.food import Food
from model.food_vendors import FoodVendor
from model.job_run import JobStatus, JobRun
from monitoring.logging import JOB_LOGGER, APP_LOGGER
from settings import SETTINGS


def run_collect_food_data_job():
    APP_LOGGER.info("🔄 Running scheduled food data fetch job...")
    with Session(engine) as session:
        CollectFoodDataJob(session, VENDOR_STRATEGIES).run()


class CollectFoodDataJob:
    def __init__(self,
                 session: Session,
                 strategies: list[FoodVendorStrategy],
                 weeks_to_fetch: int = SETTINGS.WEEKS_TO_FETCH,
                 delay: float = SETTINGS.FETCHING_DELAY,
                 fetch_images: bool = SETTINGS.FETCH_IMAGES,
                 image_dir: Path = SETTINGS.food_image_dir,
                 data_dir: Path = SETTINGS.data_dir):
        self.session = session
        self.strategies = strategies
        self.weeks_to_fetch = weeks_to_fetch
        self.delay = delay
        self.fetch_images = fetch_images
        self.image_dir = image_dir
        self.data_dir = data_dir

    def run(self):
        self._ensure_dirs_exist()
        current_year = datetime.now().year
        current_week = datetime.now().isocalendar()[1]

        for strategy in self.strategies:
            for week in range(current_week, current_week + self.weeks_to_fetch):
                try:
                    self._sync_one_week_food_data(current_year, week, strategy)
                    self._track_successful_job_run(current_year, strategy, week)
                except Exception as e:
                    self._track_failed_job_jon(current_year, e, strategy, week)

                time.sleep(self.delay)

    def _ensure_dirs_exist(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.image_dir.mkdir(parents=True, exist_ok=True)

    def _sync_one_week_food_data(self, year: int, week: int, strategy: FoodVendorStrategy):
        foods = strategy.fetch_foods_for(year, week)
        self._save_food_to_db(foods, week)

        raw_data = strategy.get_raw_data(year, week)
        self._save_foods_to_json(strategy.get_name().value, raw_data, year, week)

        # if self.fetch_images:
        #     self._download_food_images(foods, strategy)

    def _save_food_to_db(self, foods: list[Food], week: int):
        for food in foods:
            self.session.merge(food)

        self.session.commit()

        JOB_LOGGER.info(f"✅ Week {week} food selection stored in the database.")

    def _save_foods_to_json(self, vendor_name: str, data: dict, year: int, week: int):
        filename = self.data_dir / f"{vendor_name}-week-{year}-{week}.json"
        save_to_json(data, filename)

        JOB_LOGGER.info(f"✅ Week {week} data saved to {filename}.")

    def _track_successful_job_run(self, current_year, strategy, week):
        job_id = self._track_job_run(week, current_year, JobStatus.SUCCESS, strategy.get_name())
        JOB_LOGGER.info(
            f"✅ Job ID={job_id}: Successfully fetched & stored data for {strategy.get_name()} Week {week}.")

    def _track_job_run(self, week: int, year: int, status: JobStatus, vendor: FoodVendor) -> int:
        job_run = JobRun(week=week, year=year, status=status, timestamp=datetime.now(), food_vendor=vendor)
        self.session.add(job_run)
        self.session.commit()
        self.session.refresh(job_run)

        JOB_LOGGER.info(f"📌 Job Run Logged: ID={job_run.id}, Week={week}, Year={year}, Status={status}")
        return job_run.id

    def _track_failed_job_jon(self, current_year, e, strategy, week):
        job_id = self._track_job_run(week, current_year, JobStatus.FAILURE, strategy.get_name())
        JOB_LOGGER.error(f"❌ Job ID={job_id}: Unexpected error: {e}")

    def _download_food_images(self, foods: list[Food], strategy: FoodVendorStrategy):
        for food in foods:
            self._download_image(strategy.get_food_image_url(food.food_id),
                                 f"{food.food_id}_{strategy.get_name().value}.png")
            time.sleep(self.delay)

    def _download_image(self, url: str, image_name: str):
        save_path = self.image_dir / image_name
        if save_path.exists():
            JOB_LOGGER.info(f"🟡 Skipping image (already exists): {save_path}")
            return

        JOB_LOGGER.info(f"⬇️ Downloading image: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            with open(save_path, "wb") as f:
                f.write(response.content)

            JOB_LOGGER.info(f"✅ Saved image: {save_path}")
        except Exception as e:
            JOB_LOGGER.warning(f"❌ Failed to download image from {url}: {e}")


if __name__ == "__main__":
    SETTINGS.data_dir.mkdir(parents=True, exist_ok=True)

    init_db()
    with Session(engine) as job_session:
        CollectFoodDataJob(job_session, VENDOR_STRATEGIES, 1).run()
