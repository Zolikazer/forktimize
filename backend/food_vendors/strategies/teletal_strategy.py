from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from model.food import Food


class TeletalStrategy(FoodVendorStrategy):
    def __init__(self, menu_page: TeletalMenuPage, food_page: TeletalFoodPage, delay=0.3):
        self._menu_page = menu_page
        self._food_page = food_page
        self._delay = delay
        self._raw_data = None

    def fetch_foods_for(self, year: int, week: int) -> list[Food]:
        self._menu_page.load(week)
        category_codes = self._menu_page.get_food_category_codes(year, week)
        raw_food_data = []
        for code in category_codes:
            for day in range(1,5):
                self._food_page.load(year=year, week=week, day=day, category_code=code)

        pass

    def get_raw_data(self, year: int, week: int):
        return self._raw_data

    def get_food_image_url(self, food_id: int) -> str:
        pass

    def get_name(self) -> FoodVendor:
        return FoodVendor.TELETAL
