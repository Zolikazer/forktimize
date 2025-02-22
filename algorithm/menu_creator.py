from model.nutritional_constraints import NutritionalConstraints


class MenuCreator:
    def __init__(self, algorithm, nutrition_constraints: NutritionalConstraints):
        self.algorithm = algorithm
        self.nutrition_constraints = nutrition_constraints

    def create_menu(self, foods):
        return self.algorithm.run(foods, self.nutrition_constraints)
