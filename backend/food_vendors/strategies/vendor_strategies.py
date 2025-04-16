from food_vendors.strategies.inter_city_food.city_food_strategy import CityFoodStrategy
from food_vendors.strategies.inter_city_food.inter_food_strategy import InterFoodStrategy
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from food_vendors.strategies.teletal.teletal_strategy import TeletalStrategy
from settings import SETTINGS

VENDOR_STRATEGIES = [
    CityFoodStrategy(),
    InterFoodStrategy(),
]


def get_vendor_strategies():
    vendor_strategies = [
        CityFoodStrategy(),
        InterFoodStrategy(),
    ]
    if SETTINGS.INCLUDE_HEAVY_JOBS:
        client = TeletalClient("https://www.teletal.hu/etlap", "https://www.teletal.hu/ajax")
        vendor_strategies.append(TeletalStrategy(TeletalMenuPage(client), TeletalFoodPage(client)))

    return vendor_strategies