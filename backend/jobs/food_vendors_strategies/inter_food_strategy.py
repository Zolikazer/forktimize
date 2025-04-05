from model.food_vendors import FoodVendor
from jobs.food_vendors_strategies.inter_city_food_strategy import InterCityFoodStrategy
from settings import SETTINGS


class InterFoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.inter_food_menu_url, FoodVendor.INTER_FOOD)
