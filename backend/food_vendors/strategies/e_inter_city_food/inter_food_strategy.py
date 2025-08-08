from __future__ import annotations
from food_vendors.strategies.e_inter_city_food.e_inter_city_food_strategy import EInterCityFoodStrategy
from food_vendors.food_vendor_type import FoodVendorType
from settings import SETTINGS


class InterFoodStrategy(EInterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.inter_food_menu_api_url, SETTINGS.INTER_FOOD_IMAGE_URL_TEMPLATE,
                         FoodVendorType.INTER_FOOD)
