class MealPlanRequestException(Exception):
    def __init__(self, message: str, error_code: str, field=None):
        self.message = message
        self.error_code = error_code
        self.field = field
