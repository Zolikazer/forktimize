import logging
from typing import Any, Dict, Optional

from model.job_run import JobType
from monitoring.logging import JOB_LOGGER


class JobLogger:
    """
    Logger wrapper that includes job ID and context in all log messages.
    
    Provides consistent logging format: [JOB-{id}] [{job_type}] [{context}] {message}
    """
    
    def __init__(self, base_logger: logging.Logger, job_id: int, job_type: JobType, context: Optional[Dict[str, Any]] = None):
        self._logger = base_logger
        self._job_id = job_id
        self._job_type = job_type
        self._context = context or {}
    
    def _format_message(self, msg: str) -> str:
        """Format message with job ID, type, and context."""
        prefix = f"[JOB-{self._job_id}] [{self._job_type.value.upper()}]"
        
        if self._context:
            context_parts = []
            for key, value in self._context.items():
                context_parts.append(f"[{key.upper()}-{value}]")
            context_str = "".join(context_parts)
            prefix += f" {context_str}"
        
        return f"{prefix} {msg}"
    
    def debug(self, msg: str, *args, **kwargs):
        """Log debug message with job context."""
        self._logger.debug(self._format_message(msg), *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        """Log info message with job context."""
        self._logger.info(self._format_message(msg), *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        """Log warning message with job context."""
        self._logger.warning(self._format_message(msg), *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        """Log error message with job context."""
        self._logger.error(self._format_message(msg), *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        """Log critical message with job context."""
        self._logger.critical(self._format_message(msg), *args, **kwargs)


def create_job_logger(job_id: int, job_type: JobType, context: Optional[Dict[str, Any]] = None) -> JobLogger:
    """
    Factory function to create a JobLogger with consistent base logger.
    
    Args:
        job_id: The job ID to include in logs
        job_type: The job type to include in logs  
        context: Optional context dict (e.g., {"vendor": "CITY_FOOD", "week": 32})
    
    Returns:
        JobLogger instance configured with the provided parameters
    """
    return JobLogger(JOB_LOGGER, job_id, job_type, context)