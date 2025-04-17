from food_vendors.strategies.inter_city_food.inter_city_food_strategy import InterCityFoodStrategy
from food_vendors.food_vendor import FoodVendor
from settings import SETTINGS


class InterFoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.inter_food_menu_url, SETTINGS.INTER_FOOD_IMAGE_URL_TEMPLATE, FoodVendor.INTER_FOOD)

    def get_food_image_url(self, food_id: int) -> str:
        return SETTINGS.INTER_FOOD_IMAGE_URL_TEMPLATE.format(food_id=food_id)
