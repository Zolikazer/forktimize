import time
from typing import List

from pulp import LpProblem, LpMinimize, LpInteger, LpVariable, lpSum, PULP_CBC_CMD, LpStatus

from model.nutritional_constraints import NutritionalConstraints
from model.food import Food
from model.menu import Menu
from monitoring.logger import LOGGER


def create_menu(foods: List[Food], nutrition_constraints: NutritionalConstraints) -> Menu:
    problem = LpProblem("Menu_Creation_ILP", LpMinimize)

    x_vars = {food: LpVariable(f"x_{food.food_id}", lowBound=0, cat=LpInteger) for food in foods}
    problem += lpSum(x_vars[f] * f.price for f in foods), "TotalCost"

    for attr, label in [("calories", "Calories"), ("protein", "Protein"), ("carb", "Carbs"), ("fat", "Fat")]:
        _add_nutrient_constraint(foods, nutrition_constraints, problem, x_vars, attr, label)

    _add_max_occurrence_per_food_constraint(foods, nutrition_constraints, problem, x_vars)

    start_time = time.time()
    solver = PULP_CBC_CMD(msg=False)
    status = LpStatus[problem.solve(solver)]
    duration = time.time() - start_time

    if status == "Optimal":
        LOGGER.info(f"✅ Successfully created a menu in {duration:.4f} seconds.")
        return _convert_result_to_menu(foods, x_vars)
    else:
        LOGGER.info("Could not create menu. Status: %s", status)
        return Menu()


def _add_nutrient_constraint(foods, nutrition_constraints, problem, x_vars, attr_name: str, label: str):
    min_val = getattr(nutrition_constraints, f"min_{attr_name}")
    max_val = getattr(nutrition_constraints, f"max_{attr_name}")

    total_nutrient = lpSum(x_vars[f] * getattr(f, attr_name) for f in foods)

    if min_val is not None:
        problem += total_nutrient >= min_val, f"Min{label}"
    if max_val is not None:
        problem += total_nutrient <= max_val, f"Max{label}"


def _convert_result_to_menu(foods, x_vars) -> Menu:
    menu = Menu()
    chosen_foods = {f: int(x_vars[f].varValue) for f in foods if int(x_vars[f].varValue) > 0}

    for food, qty in chosen_foods.items():
        for _ in range(qty):
            menu.add_food(food)

    return menu


def _add_max_occurrence_per_food_constraint(foods, nutrition_constraints, problem, x_vars):
    if nutrition_constraints.max_occurrences_per_food is not None:
        for f in foods:
            problem += (x_vars[f] <= nutrition_constraints.max_occurrences_per_food), f"MaxOccurEach_{f.food_id}"
    return problem
