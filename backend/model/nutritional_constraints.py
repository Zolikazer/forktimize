from typing import Optional

from pydantic import BaseModel, model_validator, PositiveInt
from typing_extensions import Self


class Square(BaseModel):
    width: float
    height: float

    @model_validator(mode='after')
    def verify_square(self) -> Self:
        if self.width != self.height:
            raise ValueError('width and height do not match')
        return self


class NutritionalConstraints(BaseModel):
    min_calories: Optional[PositiveInt] = 2300
    max_calories: Optional[PositiveInt] = 2700
    min_protein: Optional[PositiveInt] = 200
    max_protein: Optional[PositiveInt] = None
    min_carbs: Optional[PositiveInt] = None
    max_carbs: Optional[PositiveInt] = None
    min_fat: Optional[PositiveInt] = None
    max_fat: Optional[PositiveInt] = None
    max_occurrences_per_food: Optional[PositiveInt] = None

    @model_validator(mode='after')
    def _validate_min_lower_than_max(self) -> Self:
        if self.min_calories is not None and self.max_calories is not None and self.min_calories > self.max_calories:
            raise ValueError("min_calories must be less than or equal to max_calories")
        if self.min_protein is not None and self.max_protein is not None and self.min_protein > self.max_protein:
            print(self.min_protein, self.max_protein)
            raise ValueError("min_protein must be less than or equal to max_protein")
        if self.min_carbs is not None and self.max_carbs is not None and self.min_carbs > self.max_carbs:
            raise ValueError("min_carbs must be less than or equal to max_carbs")
        if self.min_fat is not None and self.max_fat is not None and self.min_fat > self.max_fat:
            raise ValueError("min_fat must be less than or equal to max_fat")

        return self

    @model_validator(mode='after')
    def _validate_macro_constraints_consistent_with_calories(self) -> Self:
        if self._all_min_macros_given():
            if self.min_carbs * 4 + self.min_fat * 9 + self.min_protein * 4 > self.min_calories:
                raise ValueError(
                    "The sum of min_carbs * 4, min_fat * 9, and min_protein * 4 must not exceed min_calories")
        if self._all_max_macros_are_given():
            if self.max_carbs * 4 + self.max_fat * 9 + self.max_protein * 4 > self.max_calories:
                raise ValueError(
                    "The sum of max_carbs * 4, max_fat * 9, and max_protein * 4 must not exceed max_calories")

        return self

    def _all_max_macros_are_given(self):
        return self.max_calories is not None and self.max_carbs is not None and self.max_fat is not None and self.max_protein is not None

    def _all_min_macros_given(self):
        return self.min_calories is not None and self.min_carbs is not None and self.min_fat is not None and self.min_protein is not None
