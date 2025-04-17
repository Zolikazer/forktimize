from datetime import datetime
from enum import Enum

from pydantic import PositiveInt
from sqlmodel import SQLModel, Field

from food_vendors.food_vendor_type import FoodVendorType


class JobStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class JobRun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    food_vendor: FoodVendorType = Field(nullable=False)
    week: PositiveInt
    year: PositiveInt
    status: JobStatus
