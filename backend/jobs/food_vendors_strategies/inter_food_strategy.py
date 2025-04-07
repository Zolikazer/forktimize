from model.food_vendors import FoodVendor
from jobs.food_vendors_strategies.inter_city_food_strategy import InterCityFoodStrategy
from settings import SETTINGS


class InterFoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.inter_food_menu_url, FoodVendor.INTER_FOOD)

    def get_food_image_url(self, food_id: int) -> str:
        return SETTINGS.INTER_FOOD_IMAGE_URL_TEMPLATE.format(food_id=food_id)
