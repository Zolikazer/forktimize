from typing import Optional, ClassVar

from pydantic import BaseModel, model_validator, PositiveInt, ConfigDict
from pydantic.alias_generators import to_camel
from typing_extensions import Self


class NutritionalConstraints(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True)

    PROTEIN_CALORIE: ClassVar[int] = 4
    CARB_CALORIE: ClassVar[int] = 4
    FAT_CALORIE: ClassVar[int] = 9

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
    def _validate_min_macro_constraints_consistent_with_calories(self) -> Self:
        if self._all_min_macros_given():
            if self._total_min_calories() > self.min_calories:
                raise ValueError(
                    f"The sum of max_carbs * {self.CARB_CALORIE}, "
                    f"max_fat * {self.FAT_CALORIE}, "
                    f"and max_protein * {self.PROTEIN_CALORIE} "
                    f"must not exceed min_calories")

        return self

    @model_validator(mode='after')
    def _validate_max_macro_constraints_consistent_with_calories(self) -> Self:
        if self._all_max_macros_given():
            if self._total_max_calories() > self.max_calories:
                raise ValueError(
                    f"The sum of max_carbs * {self.CARB_CALORIE}, "
                    f"max_fat * {self.FAT_CALORIE}, "
                    f"and max_protein * {self.PROTEIN_CALORIE} "
                    f"must not exceed max_calories")

        return self

    def _total_max_calories(self) -> int:
        return self.max_carb * self.CARB_CALORIE + self.max_fat * self.FAT_CALORIE + self.max_protein * self.PROTEIN_CALORIE

    def _total_min_calories(self) -> int:
        return self.min_carb * self.CARB_CALORIE + self.min_fat * self.FAT_CALORIE + self.min_protein * self.PROTEIN_CALORIE

    def _all_max_macros_given(self) -> bool:
        return self.max_calories is not None and self.max_carb is not None and self.max_fat is not None and self.max_protein is not None

    def _all_min_macros_given(self) -> bool:
        return self.min_calories is not None and self.min_carb is not None and self.min_fat is not None and self.min_protein is not None
