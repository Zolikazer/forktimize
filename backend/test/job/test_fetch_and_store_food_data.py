from pathlib import Path
from unittest.mock import patch, Mock, MagicMock

import pytest
from sqlalchemy import create_engine, StaticPool
from sqlmodel import select, SQLModel, Session

from jobs.fetch_food_selection_job import fetch_and_store_cityfood_data
from jobs.serialization import open_json
from model.food import Food
from model.job_run import JobRun, JobStatus
from test.food_factory import make_food


@pytest.fixture
def mock_requests_post_success():
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = open_json(
            str(Path(__file__).parent.parent.resolve() / "resources/city-response-test.json"))
        mock_response.status_code = 200
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
    strategy = MagicMock()
    strategy.fetch_foods_for.return_value = [make_food(), make_food(), make_food()]

    fetch_and_store_cityfood_data(test_session, strategy)

    job_run = test_session.exec(select(JobRun)).first()
    assert job_run.status == JobStatus.SUCCESS, "JobRun with SUCCESS not found!"

    food_entries = test_session.exec(select(Food)).all()
    assert len(food_entries) == 3, "No food entries were inserted into the database!"


def test_fetch_fails_and_marks_job_as_failed(test_session):
    strategy = MagicMock()
    strategy.fetch_foods_for.side_effect = Exception("Failed to fetch food data!")

    fetch_and_store_cityfood_data(test_session, strategy)

    job_run = test_session.exec(select(JobRun)).first()
    assert job_run.status == JobStatus.FAILURE, "JobRun with FAILURE not found!"
