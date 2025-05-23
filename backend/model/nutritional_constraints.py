from typing import Optional

from pydantic import BaseModel, model_validator, PositiveInt, ConfigDict, NonNegativeInt
from pydantic.alias_generators import to_camel
from typing_extensions import Self

from constants import PROTEIN_CALORIE, FAT_CALORIE, CARB_CALORIE
from exceptions import MealPlanRequestException


class NutritionalConstraints(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              alias_generator=to_camel,
                              populate_by_name=True,
                              frozen=True)

    min_calories: Optional[NonNegativeInt] = None
    max_calories: Optional[PositiveInt] = None
    min_protein: Optional[NonNegativeInt] = None
    max_protein: Optional[PositiveInt] = None
    min_carb: Optional[NonNegativeInt] = None
    max_carb: Optional[PositiveInt] = None
    min_fat: Optional[NonNegativeInt] = None
    max_fat: Optional[PositiveInt] = None

    @model_validator(mode='after')
    def _validate_min_lower_than_max(self) -> Self:
        for attr in ["calories", "protein", "carb", "fat"]:
            min_val = getattr(self, f"min_{attr}")
            max_val = getattr(self, f"max_{attr}")

            if min_val is not None and max_val is not None and min_val > max_val:
                raise MealPlanRequestException(f"min_{attr} must be less than or equal to max_{attr}",
                                               "max_lower_than_min", attr)

        return self

    @model_validator(mode='after')
    def _validate_min_macro_constraints_consistent_with_calories(self) -> Self:
        if self.max_calories and self._total_min_macro_calories() > self.max_calories:
            raise MealPlanRequestException("Total min macro calories exceed min_calories.", "macro_calories_conflict",
                                           "min")

        return self

    # TODO: can it be deleted?
    def _total_max_macro_calories(self) -> int:
        return self._max_carb_calories() + self._max_fat_calories() + self._max_protein_calories()

    def _max_protein_calories(self):
        return self.max_protein * PROTEIN_CALORIE if self.max_protein else 0

    def _max_fat_calories(self):
        return self.max_fat * FAT_CALORIE if self.max_fat else 0

    def _max_carb_calories(self):
        return self.max_carb * CARB_CALORIE if self.max_carb else 0

    def _total_min_macro_calories(self) -> int:
        return self._min_carbs_calories() + self._min_fat_calories() + self._min_protein_calories()

    def _min_protein_calories(self):
        return self.min_protein * PROTEIN_CALORIE if self.min_protein else 0

    def _min_fat_calories(self):
        return self.min_fat * FAT_CALORIE if self.min_fat else 0

    def _min_carbs_calories(self):
        return self.min_carb * CARB_CALORIE if self.min_carb else 0
