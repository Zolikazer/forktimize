from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field


class JobStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class JobRun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    week: int
    year: int
    status: JobStatus
