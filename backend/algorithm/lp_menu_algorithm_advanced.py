from typing import List

from pulp import LpProblem, LpMinimize, LpInteger, LpVariable, lpSum, PULP_CBC_CMD, LpStatus

from model.nutritional_constraints import NutritionalConstraints
from model.food import Food
from model.menu import Menu
from monitoring import LOGGER


def create_menu(foods: List[Food], nutrition_constraints: NutritionalConstraints) -> Menu:
    # Create the LP problem
    problem = LpProblem("Menu_Creation_ILP", LpMinimize)

    # Create an integer variable x_i for each food (0 <= x_i)
    # We won't put an explicit upper bound because sum of all x_i will be <= max_items anyway
    x_vars = {food: LpVariable(f"x_{food.food_id}", lowBound=0, cat=LpInteger)
              for food in foods}

    # ---------------------- OBJECTIVE: MINIMIZE COST ----------------------
    problem += lpSum(x_vars[f] * f.price for f in foods), "TotalCost"

    # ---------------------- CONSTRAINTS ----------------------

    # # 1) TOTAL ITEMS <= max_items
    # problem += lpSum(x_vars[f] for f in foods) <= max_items, "MaxItems"

    # 2) CALORIES in [min_cal, max_cal]
    problem = _add_calorie_constraints(foods, nutrition_constraints, problem, x_vars)

    # 3) Protein in [min_protein, max_protein] (if specified)
    problem = _add_protein_constraints(foods, nutrition_constraints, problem, x_vars)

    # 4) Carbs in [min_carbs, max_carbs] (if specified)
    problem = _add_carbs_constrains(foods, nutrition_constraints, problem, x_vars)

    # 5) Fat in [min_fat, max_fat] (if specified)
    problem = _add_fat_constraints(foods, nutrition_constraints, problem, x_vars)

    # Add a universal max occurrences constraint if desired
    problem = _add_max_occurrence_per_food_constraint(foods, nutrition_constraints, problem, x_vars)

    # ---------------------- SOLVE ----------------------
    solver = PULP_CBC_CMD(msg=False)  # msg=0 to suppress solver output

    status = LpStatus[problem.solve(solver)]

    menu = Menu()
    if status == "Optimal":
        return menu
    else:
        LOGGER.info("Could not create menu. Status: %s", status)
        return menu


def _add_max_occurrence_per_food_constraint(foods, nutrition_constraints, problem, x_vars):
    if nutrition_constraints.max_occurrences_per_food is not None:
        for f in foods:
            problem += (x_vars[f] <= nutrition_constraints.max_occurrences_per_food), f"MaxOccurEach_{f.food_id}"
    return problem


def _convert_result_to_menu(foods, menu, x_vars):
    chosen_foods = {}
    for f in foods:
        qty = int(x_vars[f].varValue)  # quantity chosen
        if qty > 0:
            chosen_foods[f] = qty
            [menu.add_food(f) for _ in range(qty)]
    return chosen_foods


def _add_fat_constraints(foods, nutrition_constraints, problem, x_vars):
    if nutrition_constraints.min_fat is not None:
        total_fat = lpSum(x_vars[f] * f.fat for f in foods)
        problem += total_fat >= nutrition_constraints.min_fat, "MinFat"
    if nutrition_constraints.max_fat is not None:
        total_fat = lpSum(x_vars[f] * f.fat for f in foods)
        problem += total_fat <= nutrition_constraints.max_fat, "MaxFat"
    return problem


def _add_carbs_constrains(foods, nutrition_constraints, problem, x_vars):
    if nutrition_constraints.min_carb is not None:
        total_carbs_ = lpSum(x_vars[f] * f.carbs for f in foods)
        problem += total_carbs_ >= nutrition_constraints.min_carb, "MinCarbs"
    if nutrition_constraints.max_carb is not None:
        total_carbs_ = lpSum(x_vars[f] * f.carbs for f in foods)
        problem += total_carbs_ <= nutrition_constraints.max_carb, "MaxCarbs"
    return problem


def _add_protein_constraints(foods, nutrition_constraints, problem, x_vars):
    if nutrition_constraints.min_protein is not None:
        total_protein = lpSum(x_vars[f] * f.protein for f in foods)
        problem += total_protein >= nutrition_constraints.min_protein, "MinProtein"
    if nutrition_constraints.max_protein is not None:
        total_protein = lpSum(x_vars[f] * f.protein for f in foods)
        problem += total_protein <= nutrition_constraints.max_protein, "MaxProtein"
    return problem


def _add_calorie_constraints(foods, nutrition_constraints, problem, x_vars):
    if nutrition_constraints.min_calories is not None:
        total_calories = lpSum(x_vars[f] * f.kcal for f in foods)
        problem += total_calories >= nutrition_constraints.min_calories, "MinCalories"
    if nutrition_constraints.max_calories is not None:
        total_calories = lpSum(x_vars[f] * f.kcal for f in foods)
        problem += total_calories <= nutrition_constraints.max_calories, "MaxCalories"
    return problem
