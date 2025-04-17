import time

from exceptions import TeletalUnavailableFoodError
from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy, StrategyResult
from food_vendors.strategies.teletal.food_model_mapper import map_to_food_model
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from jobs.file_utils import save_file
from model.food import Food
from monitoring.logging import JOB_LOGGER
from settings import SETTINGS


class TeletalStrategy(FoodVendorStrategy):
    def __init__(self,
                 menu_page: TeletalMenuPage,
                 food_page: TeletalFoodPage,
                 teletal_url: str = SETTINGS.TELETAL_URL,
                 delay=SETTINGS.FETCHING_DELAY):
        self._menu_page: TeletalMenuPage = menu_page
        self._food_page: TeletalFoodPage = food_page
        self._teletal_url: str = teletal_url
        self._delay: float = delay

    def fetch_foods_for(self, year: int, week: int) -> StrategyResult:
        category_codes = self._get_food_categories(week)
        raw_data = self._fetch_raw_food_data(year, week, category_codes)
        foods = self._convert_raw_food_to_model(raw_data)

        return StrategyResult(foods=foods, raw_data=raw_data, images=self._create_id_to_image_map(foods, raw_data))

    def get_name(self) -> FoodVendor:
        return FoodVendor.TELETAL

    def _fetch_raw_food_data(self, year: int, week: int, category_codes: list[str]) -> list[dict[str, str]]:
        raw_food_data = []
        for day in range(1, 6):
            raw_food_data.extend(self._fetch_food_for_day(year, week, day, category_codes))

        return raw_food_data

    def _fetch_food_for_day(self, year: int, week: int, day: int, category_codes: list) -> list[dict[str, str]]:
        failures = 0
        foods = []
        for code in category_codes:
            try:
                food = self._fetch_single_food(year, week, code, day)
                food["price"] = self._menu_page.get_price(code, day)
                foods.append(food)
                time.sleep(self._delay)
            except TeletalUnavailableFoodError:
                JOB_LOGGER.info(f"ℹ️ Skipping unavailable food: code={code}, day={day} — No info on page.")
            except Exception as e:
                failures += 1
                JOB_LOGGER.error(
                    f"Failed to fetch food data for year: "
                    f"{year} - "
                    f"week: {week} - "
                    f"day: {day} - "
                    f"code: {code}:"
                    f"{e}")

                self._save_for_debug(code, day)
            JOB_LOGGER.warning(f"TELETAL | Failed to fetch food data {failures} times.")

        return foods

    def _save_for_debug(self, code, day):
        save_file(self._food_page.get_raw_data(), SETTINGS.data_dir / f"teletal/debug_food_page_{code}_{day}.html")

    def _fetch_single_food(self, year: int, week: int, code: str, day: int) -> dict[str, str]:
        self._food_page.load(year=year, week=week, day=day, category_code=code)

        return self._food_page.get_food_data()

    def _get_food_categories(self, week: int) -> list[str]:
        self._menu_page.load(week)

        return self._menu_page.get_food_category_codes()

    @staticmethod
    def _convert_raw_food_to_model(raw_data: list[dict[str, str]]) -> list[Food]:
        failures = 0
        food_models = []
        for raw_food in raw_data:
            try:
                food_models.append(map_to_food_model(raw_food))
            except Exception as e:
                failures += 1
                JOB_LOGGER.error(f"Failed to convert raw food data to model: data: {raw_food} - exception: {e}")

        JOB_LOGGER.warning(f"TELETAL | Failed to convert food data {failures} times.")

        return food_models

    def _create_id_to_image_map(self, foods: list[Food], raw_data: list[dict[str, str]]) -> dict[int, str]:
        id_to_image = {}

        for food in foods:
            for raw_food in raw_data:
                if raw_food.get("name") == food.name:
                    image = raw_food.get("image")
                    if image:
                        id_to_image[food.food_id] = f"{self._teletal_url}/{image}"
                    break

        return id_to_image
