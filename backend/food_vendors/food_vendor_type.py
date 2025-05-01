from __future__ import annotations

from enum import Enum


class FoodVendorType(str, Enum):
    CITY_FOOD = "cityfood"
    INTER_FOOD = "interfood"
    TELETAL = "teletal"
    EFOOD = "efood"
