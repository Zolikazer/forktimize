from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

from model.food import Food
from food_vendors.food_vendor_type import FoodVendorType
from monitoring.logging import JOB_LOGGER
from monitoring.job_logger import JobLogger


@dataclass
class StrategyResult:
    foods: list[Food]
    images: dict[int, str]
    raw_data: dict | list
    vendor: FoodVendorType


class FoodCollectionStrategy(ABC):
    
    def __init__(self):
        self._logger: logging.Logger | JobLogger = JOB_LOGGER
    
    def set_logger(self, logger: logging.Logger | JobLogger):
        """Set logger for this strategy. Used for contextual logging in job execution."""
        self._logger = logger

    @abstractmethod
    def fetch_foods_for(self, year: int, week: int) -> StrategyResult:
        pass

    @abstractmethod
    def get_vendor(self) -> FoodVendorType:
        pass
