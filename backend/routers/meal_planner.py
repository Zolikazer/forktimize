from datetime import date

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from database.data_access import get_unique_dates_after, get_foods_for_given_date
from database.db import get_session
from model.meal_plan import MealPlan
from model.meal_plan_request import MealPlanRequest
from monitoring.logging import APP_LOGGER
from optimizers.meal_optimizer import solve_meal_plan_ilp


class AppStatus:
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"


meal_planner = APIRouter()


@meal_planner.get("/dates")
def get_available_dates(session: Session = Depends(get_session)) -> list[str]:
    return sorted([d.strftime("%Y-%m-%d") for d in get_unique_dates_after(session, date.today())])


@meal_planner.post("/meal-plan")
def generate_meal_plan(meal_plan_request: MealPlanRequest,
                       session: Session = Depends(get_session)) -> MealPlan:
    food_selection = get_foods_for_given_date(session,
                                              meal_plan_request.date,
                                              meal_plan_request.food_vendor,
                                              meal_plan_request.food_blacklist)

    if not food_selection:
        return MealPlan(foods=[])

    food_counts = solve_meal_plan_ilp(food_selection, meal_plan_request.nutritional_constraints,
                                      meal_plan_request.max_food_repeat)

    return MealPlan.from_food_counts(food_selection, food_counts, meal_plan_request.date,
                                     meal_plan_request.food_vendor)


@meal_planner.get("/health", tags=["Monitoring"])
def health_check(session: Session = Depends(get_session)) -> dict:
    try:
        session.exec(select(1)).first()

        APP_LOGGER.info("✅ Health check passed.")
        return {"status": AppStatus.HEALTHY, "database": "connected"}

    except Exception as e:
        APP_LOGGER.error(f"❌ Health check failed: {e}")
        return {"status": AppStatus.UNHEALTHY, "database": "error"}
