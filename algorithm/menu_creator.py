from typing import Optional, List

from model.food import Food


class NutritionalConstraints:
    """
    Encapsulates all min/max nutrition constraints (calories, protein, carbs, fat, etc.)
    plus a limit on the number of items.
    """

    def __init__(
            self,
            min_calories: Optional[int] = None,
            max_calories: Optional[int] = None,
            min_protein: Optional[int] = None,
            max_protein: Optional[int] = None,
            min_carbs: Optional[int] = None,
            max_carbs: Optional[int] = None,
            min_fat: Optional[int] = None,
            max_fat: Optional[int] = None,
            max_items: Optional[int] = None
    ):
        self.min_calories = min_calories
        self.max_calories = max_calories
        self.min_protein = min_protein
        self.max_protein = max_protein
        self.min_carbs = min_carbs
        self.max_carbs = max_carbs
        self.min_fat = min_fat
        self.max_fat = max_fat
        self.max_items = max_items

    def meets_constraints(self, menu: List[Food]) -> bool:
        """
        Returns True if the given menu (list of Food objects) satisfies
        all the constraints. Otherwise False.
        """
        # Quick item count check
        if self.max_items is not None and len(menu) > self.max_items:
            return False

        total_cal = sum(f.kcal for f in menu)
        total_prot = sum(f.protein for f in menu)
        total_carbs = sum(f.carbs for f in menu)
        total_fat = sum(f.fat for f in menu)

        # Check calories
        if self.min_calories is not None and total_cal < self.min_calories:
            return False
        if self.max_calories is not None and total_cal > self.max_calories:
            return False

        # Check protein
        if self.min_protein is not None and total_prot < self.min_protein:
            return False
        if self.max_protein is not None and total_prot > self.max_protein:
            return False

        # Check carbs
        if self.min_carbs is not None and total_carbs < self.min_carbs:
            return False
        if self.max_carbs is not None and total_carbs > self.max_carbs:
            return False

        # Check fat
        if self.min_fat is not None and total_fat < self.min_fat:
            return False
        if self.max_fat is not None and total_fat > self.max_fat:
            return False

        return True


class MenuCreator:
    def __init__(self, algorithm, nutrition_constraints: NutritionalConstraints):
        self.algorithm = algorithm
        self.nutrition_constraints = nutrition_constraints

    def create_menu(self, foods):
        return self.algorithm.run(foods, self.nutrition_constraints)
