from typing import Optional, ClassVar

from pydantic import BaseModel, model_validator, PositiveInt, ConfigDict, NonNegativeInt
from pydantic.alias_generators import to_camel
from typing_extensions import Self


class NutritionalConstraints(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True)

    PROTEIN_CALORIE: ClassVar[int] = 4
    CARB_CALORIE: ClassVar[int] = 4
    FAT_CALORIE: ClassVar[int] = 9

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
                raise ValueError(f"min_{attr} must be less than or equal to max_{attr}")

        return self

    @model_validator(mode='after')
    def _validate_min_macro_constraints_consistent_with_calories(self) -> Self:
        if self.min_calories and self._total_min_macro_calories() > self.min_calories:
            raise ValueError("Total min macro calories exceed min_calories.")

        if self.max_calories and self._total_max_macro_calories() > self.max_calories:
            raise ValueError("Total max macro calories exceed max_calories.")
        return self

    def _total_max_macro_calories(self) -> int:
        return self._max_carb_calories() + self._max_fat_calories() + self._max_protein_calories()

    def _max_protein_calories(self):
        return self.max_protein * self.PROTEIN_CALORIE if self.max_protein else 0

    def _max_fat_calories(self):
        return self.max_fat * self.FAT_CALORIE if self.max_fat else 0

    def _max_carb_calories(self):
        return self.max_carb * self.CARB_CALORIE if self.max_carb else 0

    def _total_min_macro_calories(self) -> int:
        return self._min_carbs_calories() + self._min_fat_calories() + self._min_protein_calories()

    def _min_protein_calories(self):
        return self.min_protein * self.PROTEIN_CALORIE if self.min_protein else 0

    def _min_fat_calories(self):
        return self.min_fat * self.FAT_CALORIE if self.min_fat else 0

    def _min_carbs_calories(self):
        return self.min_carb * self.CARB_CALORIE if self.min_carb else 0
