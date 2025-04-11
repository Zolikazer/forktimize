import hashlib
import re
from datetime import datetime

from food_vendors.food_vendor import FoodVendor
from model.food import Food


def map_to_food_model(food_data: dict[str, str]) -> Food:
    return Food(
        food_id=_create_id(food_data["name"], FoodVendor.TELETAL.value),
        date=_to_date(int(food_data["year"]), int(food_data["week"]), int(food_data["day"])),
        food_vendor=FoodVendor.TELETAL,
        name=food_data["name"],
        calories=_macro_to_int(food_data["calories"]),
        protein=_macro_to_int(food_data["protein"]),
        carb=_macro_to_int(food_data["carb"]),
        fat=_macro_to_int(food_data["fat"]),
        price=_price_to_int(food_data["price"]),
    )


def _macro_to_int(value: str) -> int:
    return int(value.split(".")[0].replace(",", ""))


def _price_to_int(value: str | None) -> int:
    if not value:
        return 0
    return int(re.sub(r"[^\d]", "", value))


def _to_date(year: int, week: int, day: int) -> datetime.date:
    return datetime.fromisocalendar(year, week, day).date()


def _create_id(food_name: str, food_vendor: str) -> int:
    key = f"{food_name}|{food_vendor}"
    hash_object = hashlib.sha256(key.encode("utf-8"))
    numeric_id = int(hash_object.hexdigest(), 16)

    return int(str(numeric_id)[:12])
