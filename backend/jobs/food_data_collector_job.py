import os
import random
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from sqlmodel import Session

from database.db import ENGINE, init_db
from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from food_vendors.strategies.teletal.teletal_strategy import TeletalStrategy
from food_vendors.strategies.vendor_strategies import get_vendor_strategies
from jobs.file_utils import save_to_json, save_image
from model.food import Food
from model.job_run import JobStatus, JobRun
from monitoring.logging import JOB_LOGGER, APP_LOGGER
from monitoring.performance import benchmark
from settings import SETTINGS


@benchmark
def run_collect_food_data_job():
    APP_LOGGER.info("🔄 Running scheduled food data fetch job...")
    with Session(ENGINE) as session:
        FoodDataCollectorJob(session, get_vendor_strategies()).run()


class FoodDataCollectorJob:
    FORKTIMIZE_HEADERS = {
        "User-Agent": "ForktimizeBot/1.0 (+https://forktimize.xyz/bot-info)",
        "From": "spagina.zoltan@gmail.com",
        "X-Forktimize-Purpose": "Meal planning helper, not scraping for resale or spam. Contact: forktimize.xyz"
    }

    def __init__(self,
                 session: Session,
                 strategies: list[FoodVendorStrategy],
                 weeks_to_fetch: int = SETTINGS.WEEKS_TO_FETCH,
                 delay: float = SETTINGS.FETCHING_DELAY,
                 fetch_images: bool = SETTINGS.FETCH_IMAGES,
                 image_dir: Path = SETTINGS.food_image_dir,
                 data_dir: Path = SETTINGS.data_dir):
        self._session = session
        self._strategies = strategies
        self._weeks_to_fetch = weeks_to_fetch
        self._delay = delay
        self._fetch_images = fetch_images
        self._image_dir = image_dir
        self._data_dir = data_dir

    def run(self):
        self._ensure_dirs_exist()
        current_year = datetime.now().year
        current_week = datetime.now().isocalendar()[1]

        for strategy in self._strategies:
            for week in range(current_week, current_week + self._weeks_to_fetch):
                try:
                    self._sync_one_week_food_data(current_year, week, strategy)
                    self._track_successful_job_run(current_year, strategy, week)
                except Exception as e:
                    self._track_failed_job_run(current_year, e, strategy, week)

                time.sleep(self._delay)

    def _ensure_dirs_exist(self):
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._image_dir.mkdir(parents=True, exist_ok=True)

    def _sync_one_week_food_data(self, year: int, week: int, strategy: FoodVendorStrategy):
        result = strategy.fetch_foods_for(year, week)
        self._save_food_to_db(result.foods, week)

        self._save_foods_to_json(strategy.get_name().value, result.raw_data, year, week)

        if self._fetch_images:
            self._download_food_images(result.images, strategy.get_name())

    def _save_food_to_db(self, foods: list[Food], week: int):
        for food in foods:
            self._session.merge(food)

        self._session.commit()

        JOB_LOGGER.info(f"✅ Week {week} food selection stored in the database.")

    def _save_foods_to_json(self, vendor_name: str, data: dict, year: int, week: int):
        filename = self._data_dir / f"{vendor_name}-week-{year}-{week}.json"
        save_to_json(data, filename)

        JOB_LOGGER.info(f"✅ Week {week} data saved to {filename}.")

    def _track_successful_job_run(self, current_year, strategy, week):
        job_id = self._track_job_run(week, current_year, JobStatus.SUCCESS, strategy.get_name())
        JOB_LOGGER.info(
            f"✅ Job ID={job_id}: Successfully fetched & stored data for {strategy.get_name()} Week {week}.")

    def _track_job_run(self, week: int, year: int, status: JobStatus, vendor: FoodVendor) -> int:
        job_run = JobRun(week=week, year=year, status=status, timestamp=datetime.now(), food_vendor=vendor)
        self._session.add(job_run)
        self._session.commit()
        self._session.refresh(job_run)

        JOB_LOGGER.info(f"📌 Job Run Logged: ID={job_run.id}, Week={week}, Year={year}, Status={status}")
        return job_run.id

    def _track_failed_job_run(self, current_year, e, strategy, week):
        job_id = self._track_job_run(week, current_year, JobStatus.FAILURE, strategy.get_name())
        JOB_LOGGER.error(f"❌ Job ID={job_id}: Unexpected error: {e}")

    def _download_food_images(self, images: dict[int, str], vendor: FoodVendor):
        for food_id, image in images.items():
            ext = self._get_image_extension(image)
            self._download_image(image,
                                 f"{vendor.value}_{food_id}{ext}")
            time.sleep(self._delay + random.uniform(0.1, 0.5))

    @staticmethod
    def _get_image_extension(image_url):
        parsed = urlparse(image_url)
        _, ext = os.path.splitext(parsed.path)
        return ext if ext else ".png"

    def _download_image(self, url: str, image_name: str):
        image_path = self._image_dir / image_name
        if image_path.exists():
            JOB_LOGGER.info(f"🟡 Skipping image (already exists): {image_path}")
            return

        JOB_LOGGER.info(f"⬇️ Downloading image: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            save_image(response.content, image_path)

            JOB_LOGGER.info(f"✅ Saved image: {image_path}")
        except Exception as e:
            JOB_LOGGER.warning(f"❌ Failed to download image from {url}: {e}")


if __name__ == "__main__":
    SETTINGS.data_dir.mkdir(parents=True, exist_ok=True)
    init_db()
    client = TeletalClient("https://www.teletal.hu/etlap", "https://www.teletal.hu/ajax")
    with Session(ENGINE) as job_session:
        FoodDataCollectorJob(job_session, [TeletalStrategy(TeletalMenuPage(client), TeletalFoodPage(client))], 1).run()
