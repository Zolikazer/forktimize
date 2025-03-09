from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from monitoring.logger import LoggingMiddleware
from routers.menu_routes import router

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
