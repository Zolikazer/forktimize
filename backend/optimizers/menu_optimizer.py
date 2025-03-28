import time
from typing import List

from pulp import LpProblem, LpMinimize, LpInteger, LpVariable, lpSum, PULP_CBC_CMD, LpStatus

from model.food import Food
from model.nutritional_constraints import NutritionalConstraints
from monitoring.logging import APP_LOGGER
from monitoring.performance import benchmark


@benchmark
def solve_menu_ilp(foods: List[Food], nutrition_constraints: NutritionalConstraints,
                   max_food_repeat: int = None) -> dict[int, int]:
    problem = LpProblem("Menu_Creation_ILP", LpMinimize)

    x_vars = {food.food_id: LpVariable(f"x_{food.food_id}", lowBound=0, cat=LpInteger) for food in foods}
    problem += lpSum(x_vars[f.food_id] * f.price for f in foods), "TotalCost"

    _add_nutrient_constraints(foods, nutrition_constraints, problem, x_vars)

    _add_max_food_repeat_constraint(foods, max_food_repeat, problem, x_vars)

    start_time = time.time()
    solver = PULP_CBC_CMD(msg=False)
    status = LpStatus[problem.solve(solver)]
    duration = time.time() - start_time

    if status == "Optimal":
        APP_LOGGER.info(f"✅ Successfully created a menu in {duration:.4f} seconds.")
        return {
            f.food_id: int(x_vars[f.food_id].varValue)
            for f in foods if x_vars[f.food_id].varValue and x_vars[f.food_id].varValue > 0
        }

    APP_LOGGER.info("Could not create menu. Status: %s", status)

    return {}


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


def _add_max_food_repeat_constraint(foods: list[Food], max_food_repeat: int, problem, x_vars):
    if max_food_repeat is not None:
        for f in foods:
            problem += (x_vars[f.food_id] <= max_food_repeat), f"MaxRepeatEach_{f.food_id}"

    return problem
