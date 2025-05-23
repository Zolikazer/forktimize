from datetime import date

from cachetools import TTLCache, cached
from sqlalchemy import String, Select
from sqlmodel import select, col, Session, cast

from model.food import Food
from food_vendors.food_vendor_type import FoodVendorType
from model.job_run import JobRun, JobStatus
from monitoring.performance import benchmark
from constants import ONE_DAY


@benchmark
@cached(TTLCache(maxsize=50, ttl=ONE_DAY),
        key=lambda session, target_date: target_date)
def get_unique_dates_after(session: Session, target_date: date) -> list[date]:
    statement = select(col(Food.date)).distinct().where(Food.date > target_date)

    return list(session.exec(statement).all())


@benchmark
@cached(
    TTLCache(maxsize=50, ttl=ONE_DAY),
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
@cached(TTLCache(maxsize=100, ttl=ONE_DAY),
        key=lambda session, target_date, food_vendor, food_blacklist=None:
        (target_date, food_vendor, tuple(food_blacklist or ())))
def get_foods_for_given_date(
        session: Session,
        target_date: date,
        food_vendor: FoodVendorType,
        food_blacklist: list[str] = None,
) -> list[Food]:
    statement = (select(Food)
                 .where(Food.date == target_date)
                 .where(Food.food_vendor == food_vendor))
    for blacklisted in (food_blacklist or []):
        statement = statement.where(cast(Food.name, String).not_like(f"%{blacklisted}%"))

    return list(session.exec(statement).all())


def has_successful_job_run(session: Session, year: int, week: int, vendor: FoodVendorType) -> bool:
    statement: Select = (select(JobRun)
                 .where(JobRun.week == week)
                 .where(JobRun.year == year)
                 .where(JobRun.food_vendor == vendor)
                 .where(JobRun.status == JobStatus.SUCCESS))

    return session.exec(statement).first() is not None


def is_database_empty(session: Session) -> bool:
    return session.query(Food).first() is None
