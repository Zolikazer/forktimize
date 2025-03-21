from datetime import date

from fastapi import APIRouter, Depends, Response
from sqlmodel import Session, select

from database.db import get_session
from model.menu import Menu
from model.menu_request import MenuRequest
from monitoring.logging import APP_LOGGER
from optimizers.menu_optimizer import create_menu
from repository.forktimize_repository import get_unique_dates_after, get_foods_for_given_date
from util import ONE_DAY


class AppStatus:
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"


planner = APIRouter()


@planner.get("/dates")
def get_available_dates(response: Response, session: Session = Depends(get_session)) -> list[str]:
    today = date.today()
    response.headers["Cache-Control"] = f"public, max-age={ONE_DAY}"

    return sorted([d.strftime("%Y-%m-%d") for d in get_unique_dates_after(session, today)])


@planner.post("/menu")
def create_menu_endpoint(menu_request: MenuRequest, session: Session = Depends(get_session)) -> Menu:
    food_selection = get_foods_for_given_date(session, menu_request.date, menu_request.food_blacklist)

    if not food_selection:
        return Menu(foods=[])

    menu = create_menu(food_selection, menu_request.nutritional_constraints)

    return menu


@planner.get("/health", tags=["Monitoring"])
def health_check(session: Session = Depends(get_session)) -> dict:
    try:
        session.exec(select(1)).first()

        APP_LOGGER.info("✅ Health check passed.")
        return {"status": AppStatus.HEALTHY, "database": "connected"}

    except Exception as e:
        APP_LOGGER.error(f"❌ Health check failed: {e}")
        return {"status": AppStatus.UNHEALTHY, "database": "error"}
