from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from jobs.base_job import BaseJob
from model.job_run import JobRun, JobType, JobStatus


# Test implementation of BaseJob for testing purposes
class TestJob(BaseJob):
    def __init__(self, session: Session, job_type: JobType = JobType.FOOD_DATA_COLLECTION):
        super().__init__(session, job_type)
        self.execute_called = False
        self.failure_context_called = False
        self.should_fail = False
        self.execution_details = {"test": "data"}
        self.failure_context = {"context": "info"}

    def _execute(self) -> dict:
        self.execute_called = True
        if self.should_fail:
            raise Exception("Test failure")
        return self.execution_details

    def _get_failure_context(self) -> dict:
        self.failure_context_called = True
        return self.failure_context


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_base_job_is_abstract():
    """Test that BaseJob cannot be instantiated directly."""
    with pytest.raises(TypeError, match="Can't instantiate abstract class BaseJob"):
        BaseJob(MagicMock(), JobType.FOOD_DATA_COLLECTION)


def test_successful_job_execution_creates_job_run(session):
    """Test that successful job execution creates a job run with success status."""
    job = TestJob(session)
    
    job.run()
    
    # Verify _execute was called
    assert job.execute_called
    
    # Verify job run was created
    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 1
    
    job_run = job_runs[0]
    assert job_run.job_type == JobType.FOOD_DATA_COLLECTION
    assert job_run.status == JobStatus.SUCCESS
    assert job_run.details == {"test": "data"}


def test_failed_job_execution_creates_failure_job_run(session):
    """Test that failed job execution creates a job run with failure status and error context."""
    job = TestJob(session)
    job.should_fail = True
    
    with pytest.raises(Exception, match="Test failure"):
        job.run()
    
    # Verify both methods were called
    assert job.execute_called
    assert job.failure_context_called
    
    # Verify failure job run was created
    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 1
    
    job_run = job_runs[0]
    assert job_run.job_type == JobType.FOOD_DATA_COLLECTION
    assert job_run.status == JobStatus.FAILURE
    assert job_run.details["error"] == "Test failure"
    assert job_run.details["context"] == "info"


def test_failure_context_is_optional(session):
    """Test that jobs work correctly even without failure context."""
    class MinimalJob(BaseJob):
        def _execute(self) -> dict:
            raise Exception("Minimal failure")
        # Note: Not overriding _get_failure_context()
    
    job = MinimalJob(session, JobType.DATABASE_BACKUP)
    
    with pytest.raises(Exception, match="Minimal failure"):
        job.run()
    
    # Verify failure job run has only error message
    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 1
    
    job_run = job_runs[0]
    assert job_run.status == JobStatus.FAILURE
    assert job_run.details == {"error": "Minimal failure"}


def test_different_job_types_are_tracked_correctly(session):
    """Test that different job types are tracked with correct job type."""
    backup_job = TestJob(session, JobType.DATABASE_BACKUP)
    collection_job = TestJob(session, JobType.FOOD_DATA_COLLECTION)
    
    backup_job.run()
    collection_job.run()
    
    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 2
    
    job_types = [jr.job_type for jr in job_runs]
    assert JobType.DATABASE_BACKUP in job_types
    assert JobType.FOOD_DATA_COLLECTION in job_types


def test_template_method_pattern_execution_order(session):
    """Test that the template method pattern executes methods in correct order."""
    execution_order = []
    
    class OrderTrackingJob(BaseJob):
        def _execute(self) -> dict:
            execution_order.append("execute")
            return {"success": True}
    
    job = OrderTrackingJob(session, JobType.FOOD_DATA_COLLECTION)
    job.run()
    
    # Only _execute should be called for successful jobs
    assert execution_order == ["execute"]
    
    # Reset and test failure path
    execution_order.clear()
    
    class FailureTrackingJob(BaseJob):
        def _execute(self) -> dict:
            execution_order.append("execute")
            raise Exception("Test")
        
        def _get_failure_context(self) -> dict:
            execution_order.append("failure_context")
            return {"test": "context"}
    
    job = FailureTrackingJob(session, JobType.FOOD_DATA_COLLECTION)
    
    with pytest.raises(Exception):
        job.run()
    
    # Both methods should be called in correct order
    assert execution_order == ["execute", "failure_context"]