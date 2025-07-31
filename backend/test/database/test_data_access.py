from datetime import date, datetime

import pytest
from sqlmodel import SQLModel, create_engine, Session, select

from database.data_access import get_unique_dates_after, get_foods_for_given_date, is_database_empty, \
    get_available_dates_for_vendor, has_successful_job_run, create_job_run, save_foods_to_db
from food_vendors.food_vendor_type import FoodVendorType
from model.food import Food
from model.job_run import JobRun, JobStatus, JobType, FoodDataCollectorDetails, DatabaseBackupDetails
from test.conftest import make_food


@pytest.fixture(scope="function")
def test_db():
    test_engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="function")
def session(test_db):
    with Session(test_db) as session:
        yield session
        session.rollback()


@pytest.fixture(autouse=True)
def seed_db_with_foods(session):
    session.add_all([
        make_food(food_id=1, date=date(2025, 3, 18)),
        make_food(food_id=2, date=date(2025, 3, 18)),
        make_food(food_id=3, date=date(2025, 3, 18)),
        make_food(food_id=4, date=date(2025, 3, 19)),
        make_food(food_id=5, date=date(2025, 3, 20), food_vendor=FoodVendorType.INTER_FOOD),
    ])
    session.commit()


def test_get_foods_for_given_date__returns_all_cityfood_on_matching_date(session):
    foods = get_foods_for_given_date(session, date(2025, 3, 18), FoodVendorType.CITY_FOOD)
    assert len(foods) == 3
    assert {f.name for f in foods} == {"Test Chicken 1", "Test Chicken 2", "Test Chicken 3"}


def test_get_foods_for_given_date__returns_empty_list_if_vendor_has_no_food(session):
    foods = get_foods_for_given_date(session, date(2025, 3, 20), FoodVendorType.CITY_FOOD)
    assert foods == []


def test_get_foods_for_given_date__filters_out_blacklisted_foods(session):
    foods = get_foods_for_given_date(
        session,
        date(2025, 3, 18),
        FoodVendorType.CITY_FOOD,
        ["Test Chicken 1", "Test Chicken 2"]
    )
    assert len(foods) == 1
    assert foods[0].name == "Test Chicken 3"


def test_get_foods_for_given_date__returns_interfood_correctly(session):
    foods = get_foods_for_given_date(session, date(2025, 3, 20), FoodVendorType.INTER_FOOD)
    assert len(foods) == 1
    assert foods[0].name == "Test Chicken 5"


def test_get_unique_dates_after__returns_distinct_future_dates(session):
    session.add_all([
        make_food(date=date(2025, 3, 18)),
        make_food(date=date(2025, 3, 19)),
        make_food(date=date(2025, 3, 19)),
        make_food(date=date(2025, 3, 20)),
    ])

    session.commit()

    result = get_unique_dates_after(session, date(2025, 3, 18))
    assert result == [date(2025, 3, 19), date(2025, 3, 20)]


def test_get_available_dates_for_vendor__returns_distinct_future_dates(session):
    session.add_all([
        make_food(date=date(2025, 3, 18), food_vendor=FoodVendorType.CITY_FOOD),
        make_food(date=date(2025, 3, 19), food_vendor=FoodVendorType.CITY_FOOD),
        make_food(date=date(2025, 3, 19), food_vendor=FoodVendorType.CITY_FOOD),
        make_food(date=date(2025, 3, 20), food_vendor=FoodVendorType.CITY_FOOD),
        make_food(date=date(2025, 3, 20), food_vendor=FoodVendorType.INTER_FOOD),

    ])

    session.commit()

    result = get_available_dates_for_vendor(session, date(2025, 3, 18), FoodVendorType.CITY_FOOD)
    assert result == [date(2025, 3, 19), date(2025, 3, 20)]

def test_is_database_empty__returns_true_when_empty(session):
    session.query(Food).delete()
    assert is_database_empty(session) is True


def test_is_database_empty__returns_false_when_food_exists(session):
    assert is_database_empty(session) is False

def test_has_successful_job_run_returns_true_when_success_exists(session):
    details = FoodDataCollectorDetails(
        food_vendor=FoodVendorType.TELETAL,
        week=10,
        year=2025
    )
    job = JobRun(
        status=JobStatus.SUCCESS,
        timestamp=datetime.now(),
        details=details.model_dump()
    )
    session.add(job)
    session.commit()

    assert has_successful_job_run(session, 2025, 10, FoodVendorType.TELETAL)


def test_has_successful_job_run_returns_false_when_none_exists(session):
    assert not has_successful_job_run(session, 2025, 99, FoodVendorType.TELETAL)


def test_create_job_run__creates_and_returns_job_run_with_correct_data(session):
    details = {"test": "data", "number": 42}
    
    job_run = create_job_run(session, JobType.DATABASE_BACKUP, JobStatus.SUCCESS, details)
    
    assert job_run.id is not None
    assert job_run.job_type == JobType.DATABASE_BACKUP
    assert job_run.status == JobStatus.SUCCESS
    assert job_run.details == details
    assert job_run.timestamp is not None


def test_create_job_run__persists_job_run_to_database(session):
    details = DatabaseBackupDetails(
        backup_filename="test-backup.db",
        bucket_name="test-bucket",
        database_size_mb=1.5,
        backup_date=date(2025, 1, 1)
    )
    
    job_run = create_job_run(session, JobType.DATABASE_BACKUP, JobStatus.FAILURE, details.model_dump(mode='json'))
    
    persisted_job = session.exec(select(JobRun).where(JobRun.id == job_run.id)).first()
    assert persisted_job is not None
    assert persisted_job.job_type == JobType.DATABASE_BACKUP
    assert persisted_job.status == JobStatus.FAILURE


def test_save_foods_to_db__saves_new_foods_to_database(session):
    new_foods = [
        make_food(food_id=100, name="New Food 1", date=date(2025, 4, 1)),
        make_food(food_id=101, name="New Food 2", date=date(2025, 4, 2))
    ]
    
    save_foods_to_db(session, new_foods)
    
    saved_foods = session.exec(select(Food).where(Food.food_id.in_([100, 101]))).all()
    assert len(saved_foods) == 2
    assert {f.name for f in saved_foods} == {"New Food 1", "New Food 2"}


def test_save_foods_to_db__updates_existing_foods_in_database(session):
    updated_food = make_food(food_id=1, name="Updated Name", date=date(2025, 3, 18))
    save_foods_to_db(session, [updated_food])
    
    persisted_food = session.exec(select(Food).where(Food.food_id == 1)).first()
    assert persisted_food.name == "Updated Name"