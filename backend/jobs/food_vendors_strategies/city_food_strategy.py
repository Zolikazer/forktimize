from model.food_vendors import FoodVendor
from jobs.food_vendors_strategies.inter_city_food_strategy import InterCityFoodStrategy
from settings import SETTINGS


class CityFoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.city_food_menu_url, FoodVendor.CITY_FOOD)
