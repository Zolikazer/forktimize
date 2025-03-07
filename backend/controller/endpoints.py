from datetime import datetime

from fastapi import APIRouter

from algorithm.lp_menu_algorithm_advanced import create_menu
from model.menu import Menu
from model.menu_request import MenuRequest
from parser import parse_json, categorize_foods_by_date, filter_out_food
from settings import settings

router = APIRouter()


@router.get("/dates")
def get_available_dates() -> list[str]:
    current_week = datetime.now().isocalendar()[1]
    foods = parse_json(f"{settings.DATA_DIR}/city-response-week-{current_week + 1}.json")
    unique_dates = {food.date.strftime("%Y-%m-%d") for food in foods}
    return sorted(unique_dates)


@router.post("/menu")
def create_menu_endpoint(menu_request: MenuRequest) -> Menu:
    week_of_the_year = datetime.strptime(menu_request.date, "%Y-%m-%d").date().isocalendar()[1]
    foods = parse_json(f"{settings.DATA_DIR}/city-response-week-{week_of_the_year}.json")
    foods_of_today = categorize_foods_by_date(foods)[menu_request.date]

    food_blacklist = ["Paradicsomsaláta", "hal", "halász", "harcsa", "tengeri", "Ecetes almapaprika", "máj",
                      "tartármártás", "Barbeque", "Ludaskása"] + menu_request.food_blacklist
    filtered_foods = filter_out_food(food_blacklist, foods_of_today)

    menu = create_menu(filtered_foods, menu_request.nutritional_constraints)
    return menu
