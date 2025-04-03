from datetime import datetime
from enum import Enum

from pydantic import PositiveInt
from sqlmodel import SQLModel, Field

from jobs.food_providers.food_providers import FoodProvider


class JobStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class JobRun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    food_provider: FoodProvider = Field(nullable=False)
    week: PositiveInt
    year: PositiveInt
    status: JobStatus
