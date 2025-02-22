from datetime import datetime

from algorithm.lp_menu_algorithm import LinerProgrammingMenuCreator
from algorithm.menu_creator import NutritionalConstraints, MenuCreator
from parser import parse_json, categorize_foods_by_date, filter_out_food

if __name__ == '__main__':
    constraints = NutritionalConstraints(min_calories=2300, max_calories=2700, min_protein=200)

    foods = parse_json("../resources/city-response-week-9.json")
    today = datetime.today().strftime("%Y-%m-%d")
    foods_of_today = categorize_foods_by_date(foods)["2025-02-27"]

    food_filter_list = ["Paradicsomsaláta", "hal", "halász", "harcsa", "tengeri", "Ecetes almapaprika", "máj",
                        "tartármártás", "Barbeque", "Ludaskása"]
    filtered_foods = filter_out_food(food_filter_list, foods_of_today)

    creator = MenuCreator(LinerProgrammingMenuCreator(), constraints)
    menu = creator.create_menu(filtered_foods)
    print(menu)
