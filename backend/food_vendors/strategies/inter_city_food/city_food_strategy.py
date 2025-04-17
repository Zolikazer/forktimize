from food_vendors.strategies.inter_city_food.inter_city_food_strategy import InterCityFoodStrategy
from food_vendors.food_vendor import FoodVendor
from settings import SETTINGS


class CityFoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.city_food_menu_url, SETTINGS.CITY_FOOD_IMAGE_URL_TEMPLATE, FoodVendor.CITY_FOOD)

    def get_food_image_url(self, food_id: int) -> str:
        return SETTINGS.CITY_FOOD_IMAGE_URL_TEMPLATE.format(food_id=food_id)
