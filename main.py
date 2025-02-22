from datetime import datetime

from algorithm.lp_menu_algorithm_advanced import LinerProgrammingMenuCreatorAdvanced
from algorithm.menu_creator import MenuCreator
from model.nutritional_constraints import NutritionalConstraints
from parser import categorize_foods_by_date, filter_out_food, parse_json

if __name__ == '__main__':
    constraints = NutritionalConstraints(min_protein=200, max_protein=300,
                                         min_carbs=360, max_carbs=450)

    foods = parse_json("resources/city-response-week-9.json")
    today = datetime.today().strftime("%Y-%m-%d")
    foods_of_today = categorize_foods_by_date(foods)["2025-02-26"]

    food_filter_list = ["Paradicsomsaláta", "hal", "halász", "harcsa", "tengeri", "Ecetes almapaprika", "máj",
                        "tartármártás", "Barbeque", "Ludaskása"]
    filtered_foods = filter_out_food(food_filter_list, foods_of_today)

    creator = MenuCreator(LinerProgrammingMenuCreatorAdvanced(), constraints)
    menu = creator.create_menu(filtered_foods)
    print(menu)
