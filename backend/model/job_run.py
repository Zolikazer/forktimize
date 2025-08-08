from datetime import datetime, date
from enum import Enum
from typing import Any

from pydantic import BaseModel, PositiveInt
from sqlmodel import SQLModel, Field, JSON

from food_vendors.food_vendor_type import FoodVendorType


class JobStatus(str, Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"


class JobType(str, Enum):
    FOOD_DATA_COLLECTION = "food_data_collection"
    DATABASE_BACKUP = "database_backup"


class FoodDataCollectorDetails(BaseModel):
    food_vendor: FoodVendorType
    week: PositiveInt
    year: PositiveInt


class DatabaseBackupDetails(BaseModel):
    backup_filename: str
    bucket_name: str
    database_size_mb: float
    backup_date: date


class JobRun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    job_type: JobType = Field(default=JobType.FOOD_DATA_COLLECTION)
    status: JobStatus
    details: dict[str, Any] | None = Field(default=None, sa_type=JSON)
