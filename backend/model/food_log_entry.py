from __future__ import annotations
from typing import ClassVar

from pydantic import BaseModel


class FoodLogEntry(BaseModel):
    CHICKEN_PROTEIN_RATIO: ClassVar[float] = 25
    CHICKEN_FAT_RATIO: ClassVar[float] = 3

    chicken: int = 0
    sugar: int = 0
    oil: int = 0

    @classmethod
    def from_macros(cls, protein: int, carb: int, fat: int) -> FoodLogEntry:
        chicken_grams = (protein / cls.CHICKEN_PROTEIN_RATIO) * 100
        chicken_fat = (chicken_grams / 100) * cls.CHICKEN_FAT_RATIO
        leftover_fat = max(0, fat - int(chicken_fat))

        return FoodLogEntry(
            chicken=int(chicken_grams),
            sugar=int(carb),
            oil=int(leftover_fat),
        )
