from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, NonNegativeInt, ConfigDict


class FoodLogEntry(BaseModel):
    model_config = ConfigDict(frozen=True)

    CHICKEN_PROTEIN_CONTENT: ClassVar[float] = 25
    CHICKEN_FAT_CONTENT: ClassVar[float] = 3

    chicken: NonNegativeInt = 0
    sugar: NonNegativeInt = 0
    oil: NonNegativeInt = 0

    @classmethod
    def from_macros(cls, protein: int, carb: int, fat: int) -> FoodLogEntry:
        chicken_grams = (protein / cls.CHICKEN_PROTEIN_CONTENT) * 100
        chicken_fat = (chicken_grams / 100) * cls.CHICKEN_FAT_CONTENT
        leftover_fat = max(0, fat - int(chicken_fat))

        return FoodLogEntry(
            chicken=int(chicken_grams),
            sugar=int(carb),
            oil=int(leftover_fat),
        )
