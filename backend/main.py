from fastapi import FastAPI

from controller.endpoints import router
from middleware.logging_middleware import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.include_router(router)
