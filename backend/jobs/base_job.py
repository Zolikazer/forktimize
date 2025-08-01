from abc import ABC, abstractmethod
from typing import Any, Dict

from sqlmodel import Session

from database.data_access import create_job_run
from model.job_run import JobStatus, JobType
from monitoring.logging import JOB_LOGGER


class BaseJob(ABC):
    """
    Abstract base class for all jobs in the system.
    
    Provides common job execution pattern with tracking and error handling.
    Subclasses only need to implement the _execute() method with their specific work logic.
    """
    
    def __init__(self, session: Session, job_type: JobType):
        self._session = session
        self._job_type = job_type

    @abstractmethod
    def _execute(self) -> Dict[str, Any]:
        """
        Execute the job-specific work and return details for job tracking.
        
        Returns:
            Dict containing job details to be stored in the job run record.
            
        Raises:
            Exception: Any exception raised will be caught by run() method and logged.
        """
        pass

    def _get_failure_context(self) -> Dict[str, Any]:
        """
        Override this method to provide additional context for job failures.
        
        Returns:
            Dict containing job-specific context to include in failure details.
        """
        return {}

    def run(self):
        """
        Main entry point for job execution.
        
        Uses template method pattern to handle common concerns:
        - Job execution via _execute()
        - Success/failure tracking
        - Consistent logging
        - Error handling
        """
        JOB_LOGGER.info(f"🔄 Starting {self._job_type.value} job...")
        
        try:
            details = self._execute()
            self._track_successful_job_run(details)
            JOB_LOGGER.info(f"✅ {self._job_type.value} job completed successfully")
            
        except Exception as e:
            self._track_failed_job_run(str(e))
            JOB_LOGGER.error(f"❌ {self._job_type.value} job failed: {e}")
            raise

    def _track_successful_job_run(self, details: Dict[str, Any]):
        """Track a successful job run with the provided details."""
        job_run = create_job_run(
            self._session,
            self._job_type,
            JobStatus.SUCCESS,
            details
        )
        JOB_LOGGER.info(f"📌 Job Run Logged: ID={job_run.id}, Status={JobStatus.SUCCESS}")

    def _track_failed_job_run(self, error_message: str):
        """Track a failed job run with the error details and job-specific context."""
        details = {"error": error_message}
        # Add job-specific context for failures
        context = self._get_failure_context()
        details.update(context)
        
        job_run = create_job_run(
            self._session,
            self._job_type,
            JobStatus.FAILURE,
            details
        )
        JOB_LOGGER.error(f"❌ Job Run Failed: ID={job_run.id}, Error: {error_message}")