from datetime import datetime, date
from enum import Enum

from fastapi import APIRouter, Depends
from sqlalchemy import String
from sqlmodel import Session, select, col, cast

from database.db import get_session
from model.food import Food
from model.menu import Menu
from model.menu_request import MenuRequest
from monitoring.logger import LOGGER
from optimizers.menu_optimizer import create_menu


class AppStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


planner = APIRouter()


@planner.get("/dates")
def get_available_dates(session: Session = Depends(get_session)) -> list[str]:
    today = date.today()
    statement = select(col(Food.date)).distinct().where(Food.date > today)
    unique_dates = session.exec(statement).all()

    return sorted([d.strftime("%Y-%m-%d") for d in unique_dates])


@planner.post("/menu")
def create_menu_endpoint(menu_request: MenuRequest, session: Session = Depends(get_session)) -> Menu:
    request_date = datetime.strptime(menu_request.date, "%Y-%m-%d").date()

    statement = select(Food).where(Food.date == request_date)
    for blacklisted in menu_request.food_blacklist:
        statement = statement.where(cast(Food.name, String).not_like(f"%{blacklisted}%"))

    foods = list(session.exec(statement).all())

    if not foods:
        return Menu(foods=[])

    menu = create_menu(foods, menu_request.nutritional_constraints)

    return menu


@planner.get("/health", tags=["Monitoring"])
def health_check(session: Session = Depends(get_session)) -> dict:
    try:
        session.exec(select(1)).first()

        LOGGER.info("✅ Health check passed.")
        return {"status": AppStatus.HEALTHY, "database": "connected"}

    except Exception as e:
        LOGGER.error(f"❌ Health check failed: {e}")
        return {"status": AppStatus.UNHEALTHY, "database": "error"}
