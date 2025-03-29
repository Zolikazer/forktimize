from pathlib import Path
from unittest.mock import patch, Mock

import pytest
from requests import Response
from sqlalchemy import create_engine, StaticPool
from sqlmodel import select, SQLModel, Session

from jobs.fetch_food_selection_job import fetch_and_store_cityfood_data
from jobs.serialization import open_json
from model.food import Food
from model.job_run import JobRun, JobStatus


@pytest.fixture
def mock_requests_post_success():
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = open_json(
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
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_fetch_and_store_food_data_success(mock_requests_post_success, test_session):
    with patch("jobs.fetch_food_selection_job.save_to_json") as mock_save_to_file:
        fetch_and_store_cityfood_data(test_session)

        mock_save_to_file.assert_called()

        job_run = test_session.exec(select(JobRun)).first()
        assert job_run.status == JobStatus.SUCCESS, "JobRun with SUCCESS not found!"

        food_entries = test_session.exec(select(Food)).all()
        assert len(food_entries) > 0, "No food entries were inserted into the database!"


def test_fetch_fails_and_marks_job_as_failed(mock_requests_post_failure, test_session):
    fetch_and_store_cityfood_data(test_session)

    job_run = test_session.exec(select(JobRun)).first()
    assert job_run.status == JobStatus.FAILURE, "JobRun with FAILURE not found!"
