import datetime


class Food:
    def __init__(self, food_id: int, name: str, kcal: int, protein: int, carbs: int, fat: int, price: int,
                 date: datetime.datetime):
        self.food_id = food_id
        self.name = name
        self.kcal = int(kcal)
        self.protein = int(protein)
        self.carbs = int(carbs)
        self.fat = int(fat)
        self.price = price
        self.date = date

    @property
    def price_per_kcal(self):
        return round(self.price / self.kcal, 2)

    @property
    def price_per_protein(self):
        if self.protein == 0:
            return None
        return round(self.price / self.protein, 2)

    @property
    def kcal_per_protein(self):
        if self.protein == 0:
            return None
        return round(self.kcal / self.protein, 2)

    def __repr__(self):
        return (f"Food(name={self.name}, food_id={self.food_id} kcal={self.kcal}, protein={self.protein}, "
                f"carbs={self.carbs}, fat={self.fat}, price={self.price}, date={self.date}, "
                f"price_per_kcal={self.price_per_kcal}, kcal_per_protein={self.kcal_per_protein}, "
                f"price_per_protein={self.price_per_protein})")
