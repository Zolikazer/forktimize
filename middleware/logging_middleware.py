import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from monitoring import logger


# Custom Middleware to Log Request & Response
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()  # Track execution time

        # Log the incoming request
        body = await request.body()
        logger.info(f"📥 Incoming request: {request.method} {request.url} | Body: {body.decode()}")

        # Process the request
        response = await call_next(request)

        process_time = time.time() - start_time  # Calculate response time
        logger.info(f"📤 Response: {response.status_code} | Time: {process_time:.2f}s")

        return response

