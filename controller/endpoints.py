from fastapi import APIRouter

from algorithm.lp_menu_algorithm_advanced import create_menu
from model.menu import Menu
from model.nutritional_constraints import NutritionalConstraints
from parser import parse_json, categorize_foods_by_date, filter_out_food

router = APIRouter()


@router.post("/menu")
def create_menu_endpoint(constraints: NutritionalConstraints):
    """
    POST JSON to /menu with constraints (min_calories, max_calories, etc.).
    Example:
    {
      "min_calories": 1200,
      "max_calories": 2000,
      "min_protein": 50,
      "max_items": 10
    }
    """

    foods = parse_json("resources/city-response-week-9.json")
    foods_of_today = categorize_foods_by_date(foods)["2025-02-24"]

    food_blacklist = ["Paradicsomsaláta", "hal", "halász", "harcsa", "tengeri", "Ecetes almapaprika", "máj",
                      "tartármártás", "Barbeque", "Ludaskása"]
    filtered_foods = filter_out_food(food_blacklist, foods_of_today)

    menu = create_menu(filtered_foods, constraints)
    [print(food) for food in menu.foods]
    return menu
