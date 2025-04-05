from model.food_providers import FoodProvider
from jobs.food_providers.inter_city_food_strategy import InterCityFoodStrategy
from settings import SETTINGS


class InterFoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.inter_food_menu_url, FoodProvider.INTER_FOOD)
