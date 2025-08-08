import traceback
from abc import ABC, abstractmethod
from typing import Any, Dict

from sqlmodel import Session

from database.data_access import create_job_run, update_job_run
from model.job_run import JobStatus, JobType
from monitoring.job_logger import create_job_logger


class BaseJob(ABC):
    """
    Abstract base class for all jobs in the system.
    
    Provides common job execution pattern with tracking and error handling.
    Subclasses only need to implement the _execute() method with their specific work logic.
    """
    
    def __init__(self, session: Session, job_type: JobType):
        self._session = session
        self._job_type = job_type
        self._job_id: int | None = None
        self._logger = None  # Will be set after job_id is available

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

    def _create_logger_context(self) -> Dict[str, Any]:
        """
        Override this method to provide context for job logging.
        
        Returns:
            Dict containing job-specific context to include in all logs.
        """
        return {}

    def run(self):
        """
        Main entry point for job execution.
        
        Uses template method pattern to handle common concerns:
        - Create job record in RUNNING state
        - Job execution via _execute()
        - Update job record to SUCCESS/FAILURE
        - Consistent logging with job ID
        - Error handling
        """
        # Create job record in RUNNING state to get job ID
        job_run = create_job_run(self._session, self._job_type, JobStatus.RUNNING, {})
        self._job_id = job_run.id
        
        # Create job logger now that we have the job ID
        logger_context = self._create_logger_context()
        self._logger = create_job_logger(self._job_id, self._job_type, logger_context)
        
        self._logger.info(f"🔄 Starting {self._job_type.value} job...")
        
        try:
            details = self._execute()
            update_job_run(self._session, self._job_id, JobStatus.SUCCESS, details)
            self._logger.info(f"✅ {self._job_type.value} job completed successfully")
            
        except Exception as e:
            error_details = {"error": str(e)}
            context = self._get_failure_context()
            error_details.update(context)
            
            update_job_run(self._session, self._job_id, JobStatus.FAILURE, error_details)
            self._logger.error(f"❌ {self._job_type.value} job failed: {e}")
            self._logger.error(f"❌ {self._job_type.value} job stacktrace:\n{traceback.format_exc()}")
            raise

