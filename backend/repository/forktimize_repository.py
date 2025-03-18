from datetime import date

from sqlalchemy import String
from sqlmodel import select, col, Session, cast

from model.food import Food
from monitoring.performance import benchmark


@benchmark
def get_unique_dates_after(session: Session, target_date: date) -> list[date]:
    statement = select(col(Food.date)).distinct().where(Food.date > target_date)
    return list(session.exec(statement).all())


@benchmark
def get_foods_for_given_date(session: Session, food_date: date, food_blacklist: list[str] = None) -> list[Food]:
    statement = select(Food).where(Food.date == food_date)
    for blacklisted in (food_blacklist or []):
        statement = statement.where(cast(Food.name, String).not_like(f"%{blacklisted}%"))

    foods = list(session.exec(statement).all())

    return foods
