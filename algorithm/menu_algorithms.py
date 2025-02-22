from abc import ABC, abstractmethod
from typing import List

from algorithm.menu_creator import NutritionalConstraints
from model.food import Food
from model.menu import Menu


class MenuCreationAlgorithm(ABC):
    @abstractmethod
    def run(self, foods: List[Food], nutrition_constraints: NutritionalConstraints) -> Menu:
        pass
