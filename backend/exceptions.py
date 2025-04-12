class MealPlanRequestException(Exception):
    def __init__(self, message: str, error_code: str, field=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.field = field

class TeletalUnavailableFoodError(Exception):
    pass