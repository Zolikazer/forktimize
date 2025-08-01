from datetime import date, datetime

from cachetools import TTLCache, cached
from sqlalchemy import String, Select, func
from sqlmodel import select, col, Session, cast

from model.food import Food
from food_vendors.food_vendor_type import FoodVendorType
from model.job_run import JobRun, JobStatus, JobType
from monitoring.performance import benchmark
from constants import ONE_DAY
from settings import SETTINGS


@benchmark
@cached(TTLCache(maxsize=SETTINGS.DEFAULT_CACHE_SIZE, ttl=SETTINGS.DEFAULT_CACHE_TTL),
        key=lambda session, target_date: target_date)
def get_unique_dates_after(session: Session, target_date: date) -> list[date]:
    statement = select(col(Food.date)).distinct().where(Food.date > target_date)

    return list(session.exec(statement).all())


@benchmark
@cached(
    TTLCache(maxsize=SETTINGS.DEFAULT_CACHE_SIZE, ttl=SETTINGS.SHORT_CACHE_TTL),
    key=lambda session, target_date, vendor_type: (target_date, vendor_type)
)
def get_available_dates_for_vendor(session: Session, target_date: date, vendor_type: FoodVendorType) -> list[date]:
    statement = (
        select(col(Food.date))
        .distinct()
        .where(Food.date > target_date)
        .where(Food.food_vendor == vendor_type)
    )
    return list(session.exec(statement).all())


@benchmark
@cached(TTLCache(maxsize=SETTINGS.LARGE_CACHE_SIZE, ttl=SETTINGS.DEFAULT_CACHE_TTL),
        key=lambda session, target_date, food_vendor: (target_date, food_vendor))
def get_foods_for_given_date(
        session: Session,
        target_date: date,
        food_vendor: FoodVendorType,
) -> list[Food]:
    statement = (select(Food)
                 .where(Food.date == target_date)
                 .where(Food.food_vendor == food_vendor))

    return list(session.exec(statement).all())


def filter_blacklisted_foods(foods: list[Food], food_blacklist: list[str] = None) -> list[Food]:
    """Filter out blacklisted foods from the given list in memory."""
    if not food_blacklist:
        return foods
    
    return [food for food in foods 
            if not any(blacklisted.lower() in food.name.lower() 
                      for blacklisted in food_blacklist)]


def has_successful_job_run(session: Session, year: int, week: int, vendor: FoodVendorType) -> bool:
    statement: Select = (select(JobRun)
                 .where(func.json_extract(JobRun.details, '$.week') == week)
                 .where(func.json_extract(JobRun.details, '$.year') == year)
                 .where(func.json_extract(JobRun.details, '$.food_vendor') == vendor.value)
                 .where(JobRun.status == JobStatus.SUCCESS))

    return session.exec(statement).first() is not None


def is_database_empty(session: Session) -> bool:
    return session.exec(select(Food)).first() is None


def create_job_run(session: Session, job_type: JobType, status: JobStatus, details: dict) -> JobRun:
    job_run = JobRun(
        job_type=job_type,
        status=status,
        timestamp=datetime.now(),
        details=details
    )
    session.add(job_run)
    session.commit()
    session.refresh(job_run)
    return job_run


def save_foods_to_db(session: Session, foods: list[Food]) -> None:
    for food in foods:
        session.merge(food)
    session.commit()
