from fastapi import FastAPI

from controller.endpoints import router

# if __name__ == '__main__':
    # constraints = NutritionalConstraints(min_protein=200, max_protein=300,
    #                                      min_carbs=360, max_carbs=450)
    #
    # foods = parse_json("resources/city-response-week-9.json")
    # foods_of_today = categorize_foods_by_date(foods)["2025-02-24"]
    #
    # food_blacklist = ["Paradicsomsaláta", "hal", "halász", "harcsa", "tengeri", "Ecetes almapaprika", "máj",
    #                   "tartármártás", "Barbeque", "Ludaskása"]
    # filtered_foods = filter_out_food(food_blacklist, foods_of_today)
    #
    # menu = create_menu(filtered_foods, constraints)
    # print(menu)
    # print("Approximate MyFitnessPal Log:", menu.to_myfitnesspal_entries())
app = FastAPI()
app.include_router(router, prefix="/users", tags=["users"])
