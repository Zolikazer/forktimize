import time

from cachetools import TTLCache, cached
from pulp import LpProblem, LpMinimize, LpInteger, LpVariable, lpSum, PULP_CBC_CMD, LpStatus

from constants import ONE_DAY
from model.food import Food
from model.nutritional_constraints import NutritionalConstraints
from monitoring.logging import APP_LOGGER
from monitoring.performance import benchmark
from settings import SETTINGS


@benchmark
@cached(TTLCache(maxsize=SETTINGS.DEFAULT_CACHE_SIZE, ttl=SETTINGS.DEFAULT_CACHE_TTL),
        key=lambda foods, nutritional_constraints, max_food_repeat: (
                tuple(foods), nutritional_constraints, max_food_repeat)
        )
def solve_meal_plan_ilp(foods: list[Food], nutrition_constraints: NutritionalConstraints,
                        max_food_repeat: int = None) -> dict[int, int]:
    problem, x_vars = _create_price_minimization_problem(foods)

    _add_nutrient_constraints_to_problem(foods, nutrition_constraints, problem, x_vars)

    _add_max_food_repeat_to_problem(foods, max_food_repeat, problem, x_vars)

    start_time = time.time()
    solver = PULP_CBC_CMD(msg=False)
    status = LpStatus[problem.solve(solver)]
    duration = time.time() - start_time

    if status == "Optimal":
        APP_LOGGER.info(f"✅ Successfully created a meal plan in {duration * 1000:.2f} ms.")
        return _get_food_counts(foods, x_vars)

    APP_LOGGER.info("Could not create meal plan. Status: %s", status)

    return {}


def _get_food_counts(foods, x_vars):
    return {
        f.food_id: int(x_vars[f.food_id].varValue)
        for f in foods if x_vars[f.food_id].varValue and x_vars[f.food_id].varValue > 0
    }


def _create_price_minimization_problem(foods) -> [LpProblem, dict]:
    problem = LpProblem("MealPlan_Generation_ILP", LpMinimize)
    x_vars = {food.food_id: LpVariable(f"x_{food.food_id}", lowBound=0, cat=LpInteger) for food in foods}
    problem += lpSum(x_vars[f.food_id] * f.price for f in foods), "TotalCost"

    return problem, x_vars


def _add_nutrient_constraints_to_problem(foods: list[Food], nutrition_constraints: NutritionalConstraints, problem,
                                         x_vars: dict):
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


def _add_max_food_repeat_to_problem(foods: list[Food], max_food_repeat: int, problem, x_vars):
    if max_food_repeat is not None:
        for f in foods:
            problem += (x_vars[f.food_id] <= max_food_repeat), f"MaxRepeatEach_{f.food_id}"
