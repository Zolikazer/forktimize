from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.e_inter_city_food.e_inter_city_food_strategy import EInterCityFoodStrategy
from settings import SETTINGS


class EfoodStrategy(EInterCityFoodStrategy):
    def __init__(self):
        super().__init__(SETTINGS.efood_food_menu_api_url, SETTINGS.EFOOD_FOOD_IMAGE_URL_TEMPLATE,
                         FoodVendorType.EFOOD)
