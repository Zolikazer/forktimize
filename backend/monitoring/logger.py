import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        body = await request.body()
        user_agent = request.headers.get("user-agent", "Unknown")
        ip_address = request.client.host if request.client else "Unknown"

        LOGGER.info(f"📥 Incoming request: {request.method} {request.url} | "
                    f"IP: {ip_address} | "
                    f"User-Agent: {user_agent} | "
                    f"Body: {body.decode()}")

        response = await call_next(request)

        process_time = time.time() - start_time
        LOGGER.info(f"📤 Response: {response.status_code} |Time: {process_time:.2f}s")

        return response
