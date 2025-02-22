from abc import ABC, abstractmethod
from typing import List

from model.nutritional_constraints import NutritionalConstraints
from model.food import Food
from model.menu import Menu


class MenuCreationAlgorithm(ABC):
    @abstractmethod
    def run(self, foods: List[Food], nutrition_constraints: NutritionalConstraints) -> Menu:
        pass
