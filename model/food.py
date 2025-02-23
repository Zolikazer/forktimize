import datetime

from pydantic import BaseModel, ConfigDict


class Food(BaseModel):
    food_id: int
    name: str
    kcal: int
    protein: float
    carbs: float
    fat: float
    price: int
    date: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def price_per_kcal(self):
        return round(self.price / self.kcal, 2)

    @property
    def price_per_protein(self):
        return 0 if self.protein == 0 else round(self.price / self.protein, 2)

    @property
    def kcal_per_protein(self):
        return 0 if self.protein == 0 else round(self.kcal / self.protein, 2)

    def __repr__(self):
        return (f"Food(name={self.name}, food_id={self.food_id} kcal={self.kcal}, protein={self.protein}, "
                f"carbs={self.carbs}, fat={self.fat}, price={self.price}, date={self.date}, "
                f"price_per_kcal={self.price_per_kcal}, kcal_per_protein={self.kcal_per_protein}, "
                f"price_per_protein={self.price_per_protein})")

    def __hash__(self):
        return hash(self.food_id)
