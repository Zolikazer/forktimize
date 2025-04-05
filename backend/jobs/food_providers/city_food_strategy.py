from model.food_providers import FoodProvider
from jobs.food_providers.inter_city_food_strategy import InterCityFoodStrategy
from settings import SETTINGS


class CityFoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.city_food_menu_url, FoodProvider.CITY_FOOD)
