from datetime import datetime
from enum import Enum

from pydantic import PositiveInt
from sqlmodel import SQLModel, Field

from food_vendors.food_vendor_type import FoodVendorType


class JobStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class JobType(str, Enum):
    FOOD_DATA_COLLECTION = "food_data_collection"
    DATABASE_BACKUP = "database_backup"


class JobRun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    job_type: JobType = Field(default=JobType.FOOD_DATA_COLLECTION)
    food_vendor: FoodVendorType = Field(nullable=False)
    week: PositiveInt
    year: PositiveInt
    status: JobStatus
