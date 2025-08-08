import logging
from unittest.mock import MagicMock

import pytest

from model.job_run import JobType
from monitoring.job_logger import JobLogger


@pytest.fixture
def mock_logger():
    """Create a mock logger for testing."""
    return MagicMock(spec=logging.Logger)


def test_job_logger_formats_message_with_job_id_and_type(mock_logger):
    """Test that JobLogger formats messages with job ID and type."""
    job_logger = JobLogger(mock_logger, 123, JobType.FOOD_DATA_COLLECTION)
    
    job_logger.info("Test message")
    
    mock_logger.info.assert_called_once_with("[JOB-123] [FOOD_DATA_COLLECTION] Test message")


def test_job_logger_formats_message_with_context(mock_logger):
    """Test that JobLogger includes context in formatted messages."""
    context = {"vendor": "CITY_FOOD", "week": 32}
    job_logger = JobLogger(mock_logger, 456, JobType.FOOD_DATA_COLLECTION, context)
    
    job_logger.info("Test message")
    
    # Should include all context parts
    called_message = mock_logger.info.call_args[0][0]
    assert "[JOB-456]" in called_message
    assert "[FOOD_DATA_COLLECTION]" in called_message
    assert "[VENDOR-CITY_FOOD]" in called_message
    assert "[WEEK-32]" in called_message
    assert "Test message" in called_message


def test_job_logger_all_log_levels(mock_logger):
    """Test that all log levels work correctly."""
    job_logger = JobLogger(mock_logger, 100, JobType.FOOD_DATA_COLLECTION)
    
    job_logger.debug("Debug message")
    job_logger.info("Info message") 
    job_logger.warning("Warning message")
    job_logger.error("Error message")
    job_logger.critical("Critical message")
    
    mock_logger.debug.assert_called_once_with("[JOB-100] [FOOD_DATA_COLLECTION] Debug message")
    mock_logger.info.assert_called_once_with("[JOB-100] [FOOD_DATA_COLLECTION] Info message")
    mock_logger.warning.assert_called_once_with("[JOB-100] [FOOD_DATA_COLLECTION] Warning message")
    mock_logger.error.assert_called_once_with("[JOB-100] [FOOD_DATA_COLLECTION] Error message")
    mock_logger.critical.assert_called_once_with("[JOB-100] [FOOD_DATA_COLLECTION] Critical message")


def test_job_logger_passes_through_args_and_kwargs(mock_logger):
    """Test that JobLogger passes through additional args and kwargs to underlying logger."""
    job_logger = JobLogger(mock_logger, 200, JobType.FOOD_DATA_COLLECTION)
    
    job_logger.info("Message with %s and %d", "string", 42, extra={"custom": "data"})
    
    mock_logger.info.assert_called_once_with(
        "[JOB-200] [FOOD_DATA_COLLECTION] Message with %s and %d", 
        "string", 
        42, 
        extra={"custom": "data"}
    )