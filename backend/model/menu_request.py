from pydantic import BaseModel, ConfigDict

from model.nutritional_constraints import NutritionalConstraints


class MenuRequest(BaseModel):
    date: str
    nutritional_constraints: NutritionalConstraints

    model_config = ConfigDict(arbitrary_types_allowed=True)
