import logging
import os
import time
from logging.handlers import RotatingFileHandler

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from settings import SETTINGS

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

os.makedirs(SETTINGS.LOG_DIR, exist_ok=True)


def _create_logger(name: str, filename: str):
    logger = logging.getLogger(f"forktimize.{name}")
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        log_file = os.path.join(SETTINGS.LOG_DIR, filename)

        handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

    return logger


API_LOGGER = _create_logger("api", SETTINGS.API_LOG_FILE)
APP_LOGGER = _create_logger("app", SETTINGS.APP_LOG_FILE)
JOB_LOGGER = _create_logger("job", SETTINGS.JOB_LOG_FILE)
PERF_LOGGER = _create_logger("perf", SETTINGS.PERF_LOG_FILE)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        body = await request.body()
        user_agent = request.headers.get("user-agent", "Unknown")

        API_LOGGER.info(f"📥 Incoming request: {request.method} {request.url} | "
                        f"IP: {get_real_ip(request)} | "
                        f"User-Agent: {user_agent} | "
                        f"Body: {body.decode()}")

        response = await call_next(request)

        process_time = time.time() - start_time
        API_LOGGER.info(f"📤 Response: {response.status_code} |Time: {process_time * 1000:.2f} ms")

        return response

def get_real_ip(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "Unknown"
