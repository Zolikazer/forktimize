import time
from typing import List

from pulp import LpProblem, LpMinimize, LpInteger, LpVariable, lpSum, PULP_CBC_CMD, LpStatus

from model.food import Food
from model.menu import Menu
from model.nutritional_constraints import NutritionalConstraints
from monitoring.logging import APP_LOGGER
from monitoring.performance import benchmark


@benchmark
def create_menu(foods: List[Food], nutrition_constraints: NutritionalConstraints) -> Menu:
    problem = LpProblem("Menu_Creation_ILP", LpMinimize)

    x_vars = {food.food_id: LpVariable(f"x_{food.food_id}", lowBound=0, cat=LpInteger) for food in foods}
    problem += lpSum(x_vars[f.food_id] * f.price for f in foods), "TotalCost"

    _add_nutrient_constraints(foods, nutrition_constraints, problem, x_vars)

    _add_max_occurrence_per_food_constraint(foods, nutrition_constraints, problem, x_vars)

    start_time = time.time()
    solver = PULP_CBC_CMD(msg=False)
    status = LpStatus[problem.solve(solver)]
    duration = time.time() - start_time

    if status == "Optimal":
        APP_LOGGER.info(f"✅ Successfully created a menu in {duration:.4f} seconds.")
        return _convert_result_to_menu(foods, x_vars)
    else:
        APP_LOGGER.info("Could not create menu. Status: %s", status)
        return Menu()


def _add_nutrient_constraints(foods: list[Food], nutrition_constraints: NutritionalConstraints, problem, x_vars: dict):
    constraints = {
        "calories": "Calories",
        "protein": "Protein",
        "carb": "Carbs",
        "fat": "Fat"
    }
    for attr, label in constraints.items():
        min_val = getattr(nutrition_constraints, f"min_{attr}")
        max_val = getattr(nutrition_constraints, f"max_{attr}")

        total_nutrient = lpSum(x_vars[f.food_id] * getattr(f, attr) for f in foods)

        if min_val is not None:
            problem += total_nutrient >= min_val, f"Min{label}"
        if max_val is not None:
            problem += total_nutrient <= max_val, f"Max{label}"


def _convert_result_to_menu(foods, x_vars) -> Menu:
    menu = Menu()
    chosen_foods = [f for f in foods if x_vars[f.food_id].varValue and int(x_vars[f.food_id].varValue) > 0]

    for food in chosen_foods:
        menu.add_foods([food] * int(x_vars[food.food_id].varValue))

    return menu


def _add_max_occurrence_per_food_constraint(foods, nutrition_constraints, problem, x_vars):
    if nutrition_constraints.max_occurrences_per_food is not None:
        for f in foods:
            problem += (x_vars[f] <= nutrition_constraints.max_occurrences_per_food), f"MaxOccurEach_{f.food_id}"
    return problem
