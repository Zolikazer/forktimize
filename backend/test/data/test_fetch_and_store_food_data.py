from pathlib import Path
from unittest.mock import patch, Mock

import pytest
from requests import Response
from sqlmodel import select, SQLModel, Session

from data.data_loader import open_file
from data.fetch_food_selection_job import fetch_and_store_food_data
from database.db import engine
from model.JobRun import JobRun, JobStatus
from model.food import Food


@pytest.fixture
def mock_requests_post_success():
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = open_file(
            str(Path(__file__).parent.parent.resolve() / "resources/city-response-test.json"))
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture
def mock_requests_post_failure():
    with patch("requests.post") as mock_post:
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = "Something went wrong"
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("Mocked error!")
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture(scope="function")
def test_session():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_fetch_and_store_food_data_success(mock_requests_post_success, test_session):
    """Test that the job fetches and stores data correctly in the real database."""
    fetch_and_store_food_data()

    job_run = test_session.exec(select(JobRun)).first()

    assert job_run.status == JobStatus.SUCCESS, "JobRun with SUCCESS not found!"

    food_entries = test_session.exec(select(Food)).all()
    assert len(food_entries) > 0, "No food entries were inserted into the database!"


def test_fetch_fails_and_marks_job_as_failed(mock_requests_post_failure, test_session):
    fetch_and_store_food_data()

    job_run = test_session.exec(select(JobRun)).first()
    assert job_run.status == JobStatus.FAILURE, "JobRun with FAILURE not found!"
