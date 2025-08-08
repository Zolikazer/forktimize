from __future__ import annotations
from food_vendors.strategies.e_inter_city_food.e_inter_city_food_strategy import EInterCityFoodStrategy
from food_vendors.food_vendor_type import FoodVendorType
from settings import SETTINGS


class CityFoodStrategy(EInterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.city_food_menu_api_url, SETTINGS.CITY_FOOD_IMAGE_URL_TEMPLATE, FoodVendorType.CITY_FOOD)
