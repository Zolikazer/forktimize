from datetime import date

from cachetools import TTLCache, cached
from sqlalchemy import String
from sqlmodel import select, col, Session, cast

from model.food import Food
from model.food_vendors import FoodVendor
from monitoring.performance import benchmark
from constants import ONE_DAY


@benchmark
@cached(TTLCache(maxsize=50, ttl=ONE_DAY),
        key=lambda session, target_date: target_date)
def get_unique_dates_after(session: Session, target_date: date) -> list[date]:
    statement = select(col(Food.date)).distinct().where(Food.date > target_date)

    return list(session.exec(statement).all())


@benchmark
@cached(TTLCache(maxsize=100, ttl=ONE_DAY),
        key=lambda session, target_date, food_vendor, food_blacklist=None:
        (target_date, food_vendor, tuple(food_blacklist or ())))
def get_foods_for_given_date(
        session: Session,
        food_date: date,
        food_vendor: FoodVendor,
        food_blacklist: list[str] = None,
) -> list[Food]:
    statement = (select(Food)
                 .where(Food.date == food_date)
                 .where(Food.food_vendor == food_vendor))
    for blacklisted in (food_blacklist or []):
        statement = statement.where(cast(Food.name, String).not_like(f"%{blacklisted}%"))

    return list(session.exec(statement).all())


def is_database_empty(session: Session) -> bool:
    return session.query(Food).first() is None
