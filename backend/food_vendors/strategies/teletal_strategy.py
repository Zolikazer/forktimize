from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_parser import TeletalParser
from model.food import Food
from food_vendors.food_vendor import FoodVendor


class TeletalStrategy(FoodVendorStrategy):
    def __init__(self, teletal_menu_url: str, client: TeletalClient, parser: TeletalParser):
        self.teletal_menu_url = teletal_menu_url
        self.client = client
        self.parser = parser

    def fetch_foods_for(self, year: int, week: int) -> list[Food]:
        main_menu_page = self.client.get_main_menu_html()


    def get_raw_data(self, year: int, week: int) -> dict:
        pass

    def get_food_image_url(self, food_id: int) -> str:
        pass

    def get_name(self) -> FoodVendor:
        return FoodVendor.TELETAL
