from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session

from database.db import engine
from jobs.fetch_food_selection_job import fetch_and_store_food_selection
from jobs.food_providers.inter_city_food_provider import InterCityFoodProvider
from model.food import FoodProvider
from monitoring.logging import APP_LOGGER
from settings import SETTINGS

scheduler = BackgroundScheduler()

providers = [
    InterCityFoodProvider(SETTINGS.CITY_FOOD_MENU_URL, FoodProvider.CITY_FOOD),
    InterCityFoodProvider(SETTINGS.INTER_FOOD_MENU_URL, FoodProvider.INTER_FOOD),
]


def run_fetch_job():
    APP_LOGGER.info("🔄 Running scheduled food data fetch job...")
    with Session(engine) as session:
        for provider in providers:
            fetch_and_store_food_selection(session, provider)
