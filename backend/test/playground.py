from algorithm.lp_menu_algorithm_advanced import create_menu
from model.nutritional_constraints import NutritionalConstraints
from data.parser import parse_json, categorize_foods_by_date, filter_out_food

if __name__ == "__main__":
    constraints = NutritionalConstraints(min_protein=200, min_calories=2300, max_calories=2700)

    foods = parse_json("../resources/city-response-week-9.json")
    foods_of_today = categorize_foods_by_date(foods)["2025-02-24"]

    food_blacklist = ["Paradicsomsaláta", "hal", "halász", "harcsa", "tengeri", "Ecetes almapaprika", "máj",
                      "tartármártás", "Barbeque", "Ludaskása"]
    filtered_foods = filter_out_food(food_blacklist, foods_of_today)

    menu = create_menu(filtered_foods, constraints)
    print(menu)
    print("Approximate MyFitnessPal Log:", menu.to_myfitnesspal_entries())
