import time

from exceptions import TeletalUnavailableFoodError
from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy
from food_vendors.strategies.teletal.food_model_mapper import map_to_food_model
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from jobs.serialization import save_file
from model.food import Food
from monitoring.logging import JOB_LOGGER
from settings import SETTINGS


class TeletalStrategy(FoodVendorStrategy):
    def __init__(self, menu_page: TeletalMenuPage, food_page: TeletalFoodPage, delay=SETTINGS.FETCHING_DELAY):
        self._menu_page: TeletalMenuPage = menu_page
        self._food_page: TeletalFoodPage = food_page
        self._delay: float = delay
        self._raw_food_data: list[dict[str, str]] | None = None
        self._year: int | None = None
        self._week: int | None = None
        self._failures: int = 0

    def fetch_foods_for(self, year: int, week: int) -> list[Food]:
        self._failures = 0
        self._year = year
        self._week = week

        category_codes = self._get_food_categories()
        self._raw_food_data = self._fetch_raw_food_data(category_codes)

        return self._convert_raw_food_to_model()

    def get_raw_data(self) -> list[dict[str, str]]:
        return self._raw_food_data

    def get_name(self) -> FoodVendor:
        return FoodVendor.TELETAL

    def get_food_image_url(self, food_id: int) -> str:
        pass

    def _fetch_raw_food_data(self, category_codes: list[str]) -> list[dict[str, str]]:
        raw_food_data = []
        for day in range(1, 6):
            for code in category_codes:
                try:
                    food = self._fetch_single_food(code, day)
                    food["price"] = self._menu_page.get_price(code, day)
                    raw_food_data.append(food)
                    time.sleep(self._delay)
                    # TODO test it
                except TeletalUnavailableFoodError:
                    JOB_LOGGER.info(f"ℹ️ Skipping unavailable food: code={code}, day={day} — No info on page.")
                except Exception as e:
                    self._failures += 1
                    JOB_LOGGER.error(
                        f"Failed to fetch food data for year: "
                        f"{self._year} - "
                        f"week: {self._week} - "
                        f"day: {day} - "
                        f"code: {code}:"
                        f"{e}")

                    self._save_for_debug(code, day)

        return raw_food_data

    def _save_for_debug(self, code, day):
        save_file(self._food_page.get_raw_data(), SETTINGS.data_dir / f"teletal/debug_food_page_{code}_{day}.html")

    def _fetch_single_food(self, code: str, day: int) -> dict[str, str]:
        self._food_page.load(year=self._year, week=self._week, day=day, category_code=code)

        return self._food_page.get_food_data()

    def _get_food_categories(self) -> list[str]:
        self._menu_page.load(self._week)

        return self._menu_page.get_food_category_codes()

    def _convert_raw_food_to_model(self) -> list[Food]:
        food_models = []
        for raw_food in self._raw_food_data:
            try:
                food_models.append(map_to_food_model(raw_food))
            except Exception as e:
                self._failures += 1
                JOB_LOGGER.error(f"Failed to convert raw food data to model: data: {raw_food} - exception: {e}")

        return food_models
