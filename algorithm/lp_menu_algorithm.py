from typing import List

from pulp import LpProblem, LpMinimize, LpVariable, lpSum

from algorithm.menu_algorithms import MenuCreationAlgorithm
from algorithm.menu_creator import NutritionalConstraints
from model.food import Food
from model.menu import Menu


class LinerProgrammingMenuCreator(MenuCreationAlgorithm):
    def run(self, foods: List[Food], nutrition_constraints: NutritionalConstraints) -> Menu:
        foods_dict = self._convert_to_dict(foods)

        # Define the LP problem
        problem = LpProblem("Minimize_Cost", LpMinimize)

        # Decision variables (number of servings, continuous for now)
        food_vars = {name: LpVariable(name, lowBound=0, cat='Integer') for name in foods_dict}

        # Objective function: Minimize cost
        problem += lpSum(food_vars[f] * foods_dict[f]["price"] for f in foods_dict), "Total_Cost"

        # Constraints
        problem += lpSum(food_vars[f] * foods_dict[f]["protein"] for f in
                         foods_dict) >= nutrition_constraints.min_protein, "Protein_Requirement"
        problem += lpSum(
            food_vars[f] * foods_dict[f]["kcal"] for f in foods_dict) >= nutrition_constraints.min_calories, "Min_Calories"
        problem += lpSum(
            food_vars[f] * foods_dict[f]["kcal"] for f in foods_dict) <= nutrition_constraints.max_calories, "Max_Calories"
        # problem += lpSum(food_vars[f] * foods_dict[f][2] for f in foods_dict) <= 100, "Max_Fat"

        # Solve the problem
        problem.solve()

        # Display results
        print("Optimal Food Combination:")
        for f in foods_dict:
            if food_vars[f].varValue > 0:
                print(f"{f}: {food_vars[f].varValue:.2f} servings")

        print(f"Total Cost: ${problem.objective.value():.2f}")

        return self._convert_result_to_menu([food.__dict__ for food in foods], food_vars)

    def _convert_to_dict(self, foods: List[Food]) -> dict:
        return {str(food.food_id): food.__dict__ for food in foods}

    def _convert_result_to_menu(self, foods: List[dict], food_vars2: dict) -> Menu:
        foods_in_menu = list()
        for food in foods:
            servings = food_vars2[str(food['food_id'])].varValue
            if servings and servings > 0:
                for i in range(int(servings)):
                    foods_in_menu.append(Food(**food))

        return Menu(foods_in_menu)
