from datetime import datetime
from enum import Enum

from pydantic import PositiveInt
from sqlmodel import SQLModel, Field

from model.food_vendors import FoodVendor


class JobStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class JobRun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    food_vendor: FoodVendor = Field(nullable=False)
    week: PositiveInt
    year: PositiveInt
    status: JobStatus
