from model.food_vendors import FoodVendor
from jobs.food_vendors_strategies.inter_city_food_strategy import InterCityFoodStrategy
from settings import SETTINGS


class CityFoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.city_food_menu_url, FoodVendor.CITY_FOOD)

    def get_food_image_url(self, food_id: int) -> str:
        return SETTINGS.CITY_FOOD_IMAGE_URL_TEMPLATE.format(food_id=food_id)
