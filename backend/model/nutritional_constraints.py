from typing import Optional

from pydantic import BaseModel, model_validator, PositiveInt, ConfigDict
from typing_extensions import Self


def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class NutritionalConstraints(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True)

    min_calories: Optional[PositiveInt] = 2300
    max_calories: Optional[PositiveInt] = 2700
    min_protein: Optional[PositiveInt] = 200
    max_protein: Optional[PositiveInt] = None
    min_carb: Optional[PositiveInt] = None
    max_carb: Optional[PositiveInt] = None
    min_fat: Optional[PositiveInt] = None
    max_fat: Optional[PositiveInt] = None
    max_occurrences_per_food: Optional[PositiveInt] = None

    @model_validator(mode='after')
    def _validate_min_lower_than_max(self) -> Self:
        """Ensure min values are always less than max values."""
        constraints = [("calories", self.min_calories, self.max_calories),
                       ("protein", self.min_protein, self.max_protein),
                       ("carb", self.min_carb, self.max_carb),
                       ("fat", self.min_fat, self.max_fat)]

        for name, min_val, max_val in constraints:
            if min_val is not None and max_val is not None and min_val > max_val:
                raise ValueError(f"min_{name} must be less than or equal to max_{name}")

        return self

    @model_validator(mode='after')
    def _validate_macro_constraints_consistent_with_calories(self) -> Self:
        if self._all_min_macros_given():
            if self.min_carb * 4 + self.min_fat * 9 + self.min_protein * 4 > self.min_calories:
                raise ValueError(
                    "The sum of min_carbs * 4, min_fat * 9, and min_protein * 4 must not exceed min_calories")
        if self._all_max_macros_are_given():
            if self.max_carb * 4 + self.max_fat * 9 + self.max_protein * 4 > self.max_calories:
                raise ValueError(
                    "The sum of max_carbs * 4, max_fat * 9, and max_protein * 4 must not exceed max_calories")

        return self

    def _all_max_macros_are_given(self):
        return self.max_calories is not None and self.max_carb is not None and self.max_fat is not None and self.max_protein is not None

    def _all_min_macros_given(self):
        return self.min_calories is not None and self.min_carb is not None and self.min_fat is not None and self.min_protein is not None
