from typing import Optional


class NutritionalConstraints:
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
            max_occurrences_per_food: Optional[int] = None
    ):
        self.min_calories = min_calories
        self.max_calories = max_calories
        self.min_protein = min_protein
        self.max_protein = max_protein
        self.min_carbs = min_carbs
        self.max_carbs = max_carbs
        self.min_fat = min_fat
        self.max_fat = max_fat
        self.max_occurrences_per_food = max_occurrences_per_food

        self._validate_min_lower_than_max()
        self._validate_macro_constraints_consistent_with_calories()

    def _validate_min_lower_than_max(self):
        if self.min_calories is not None and self.max_calories is not None and self.min_calories > self.max_calories:
            raise ValueError("min_calories must be less than or equal to max_calories")
        if self.min_protein is not None and self.max_protein is not None and self.min_protein > self.max_protein:
            raise ValueError("min_protein must be less than or equal to max_protein")
        if self.min_carbs is not None and self.max_carbs is not None and self.min_carbs > self.max_carbs:
            raise ValueError("min_carbs must be less than or equal to max_carbs")
        if self.min_fat is not None and self.max_fat is not None and self.min_fat > self.max_fat:
            raise ValueError("min_fat must be less than or equal to max_fat")

    def _validate_macro_constraints_consistent_with_calories(self):
        if self._all_min_macros_given():
            if self.min_carbs * 4 + self.min_fat * 9 + self.min_protein * 4 > self.min_calories:
                raise ValueError(
                    "The sum of min_carbs * 4, min_fat * 9, and min_protein * 4 must not exceed min_calories")
        if self._all_max_macros_are_given():
            if self.max_carbs * 4 + self.max_fat * 9 + self.max_protein * 4 > self.max_calories:
                raise ValueError(
                    "The sum of max_carbs * 4, max_fat * 9, and max_protein * 4 must not exceed max_calories")

    def _all_max_macros_are_given(self):
        return self.max_calories is not None and self.max_carbs is not None and self.max_fat is not None and self.max_protein is not None

    def _all_min_macros_given(self):
        return self.min_calories is not None and self.min_carbs is not None and self.min_fat is not None and self.min_protein is not None
