from jobs.food_providers.food_providers import FoodProvider
from jobs.food_providers.inter_city_food_strategy import InterCityFoodStrategy
from settings import SETTINGS


class CityFoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.CITY_FOOD_MENU_URL, FoodProvider.CITY_FOOD)
