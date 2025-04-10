from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from food_vendors.strategies.teletal.teletal_parser import TeletalParser
from model.food import Food


class TeletalStrategy(FoodVendorStrategy):
    def __init__(self, client: TeletalClient, menu_page: TeletalMenuPage, delay=0.3):
        self._client = client
        self._menu_page = menu_page
        self._delay = delay
        self.raw_data = None
        self.failures = 0

    def fetch_foods_for(self, year: int, week: int) -> list[Food]:
        pass

    def get_raw_data(self, year: int, week: int):
        return self.raw_data

    def get_food_image_url(self, food_id: int) -> str:
        pass

    def get_name(self) -> FoodVendor:
        return FoodVendor.TELETAL

    def _to_int(self, nutritional_value: str):
        return int(nutritional_value.split(".")[0].replace(",", ""))
