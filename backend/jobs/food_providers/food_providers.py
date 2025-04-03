from enum import Enum


class FoodProvider(str, Enum):
    CITY_FOOD = "cityfood"
    INTER_FOOD = "interfood"
