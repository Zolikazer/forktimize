from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.inter_city_food.inter_city_food_strategy import InterCityFoodStrategy
from settings import SETTINGS


class EfoodStrategy(InterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.efood_food_menu_api_url, SETTINGS.EFOOD_FOOD_IMAGE_URL_TEMPLATE,
                         FoodVendorType.EFOOD)
