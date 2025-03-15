from datetime import datetime, date

from fastapi import APIRouter, Depends
from sqlalchemy import String
from sqlmodel import Session, select, col, cast

from database.db import get_session
from model.food import Food
from model.menu import Menu
from model.menu_request import MenuRequest
from optimizers.menu_optimizer import create_menu

router = APIRouter()


@router.get("/dates")
def get_available_dates(session: Session = Depends(get_session)) -> list[str]:
    today = date.today()
    statement = select(col(Food.date)).distinct().where(Food.date > today)
    unique_dates = session.exec(statement).all()

    return sorted([d.strftime("%Y-%m-%d") for d in unique_dates])


@router.post("/menu")
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
