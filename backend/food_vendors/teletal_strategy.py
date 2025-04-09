from food_vendors.food_vendor_strategy import FoodVendorStrategy
from food_vendors.teletal.teletal_client import TeletalClient
from model.food import Food
from food_vendors.food_vendor import FoodVendor


class TeletalStrategy(FoodVendorStrategy):
    def __init__(self, teletal_menu_url: str, client: TeletalClient, parser: TeletalParser):
        self.teletal_menu_url = teletal_menu_url

    def fetch_foods_for(self, year: int, week: int) -> list[Food]:
        pass

    def get_raw_data(self, year: int, week: int) -> dict:
        pass

    def get_food_image_url(self, food_id: int) -> str:
        pass

    def get_name(self) -> FoodVendor:
        return FoodVendor.TELETAL
