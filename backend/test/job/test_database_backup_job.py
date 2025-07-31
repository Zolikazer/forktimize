from datetime import date, datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine
from sqlmodel import select, SQLModel, Session

from jobs.database_backup_job import DatabaseBackupJob
from model.job_run import JobRun, JobStatus, JobType, DatabaseBackupDetails


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def mock_storage_client():
    client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    
    client.bucket.return_value = bucket
    bucket.blob.return_value = blob
    
    return client, bucket, blob


@pytest.fixture
def temp_db_file():
    with TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        content = "fake database content for testing" * 4000  
        db_path.write_text(content)
        yield db_path


@patch("jobs.database_backup_job.storage.Client")
def test_successful_backup_creates_job_run_entry(mock_client_class, session, temp_db_file, mock_storage_client):
    mock_client, mock_bucket, mock_blob = mock_storage_client
    mock_client_class.return_value = mock_client
    
    job = DatabaseBackupJob(
        session=session,
        bucket_name="test-bucket",
        file_prefix="test-backup",
        database_path=str(temp_db_file)
    )
    
    job.run()
    
    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 1
    
    job_run = job_runs[0]
    assert job_run.job_type == JobType.DATABASE_BACKUP
    assert job_run.status == JobStatus.SUCCESS
    assert job_run.details is not None
    
    details = DatabaseBackupDetails(**job_run.details)
    assert details.backup_filename.startswith("test-backup-")
    assert details.backup_filename.endswith(".db")
    assert details.bucket_name == "test-bucket"
    assert isinstance(details.backup_date, date)
    assert details.database_size_mb >= 0.1


@patch("jobs.database_backup_job.storage.Client")  
def test_backup_uploads_to_correct_gcp_path(mock_client_class, session, temp_db_file, mock_storage_client):
    mock_client, mock_bucket, mock_blob = mock_storage_client
    mock_client_class.return_value = mock_client
    
    job = DatabaseBackupJob(
        session=session,
        bucket_name="my-backup-bucket",
        file_prefix="forktimize-backup",
        database_path=str(temp_db_file)
    )
    
    job.run()
    
    mock_client.bucket.assert_called_once_with("my-backup-bucket")
    call_args = mock_bucket.blob.call_args[0][0]
    assert call_args.startswith("forktimize-backup-")
    assert call_args.endswith(".db")
    mock_blob.upload_from_filename.assert_called_once_with(str(temp_db_file))


@patch("jobs.database_backup_job.storage.Client")
def test_backup_skips_when_recent_backup_exists(mock_client_class, session, temp_db_file, mock_storage_client):
    mock_client, mock_bucket, mock_blob = mock_storage_client
    mock_client_class.return_value = mock_client
    
    # Create an existing successful backup from 3 days ago
    existing_backup = JobRun(
        job_type=JobType.DATABASE_BACKUP,
        status=JobStatus.SUCCESS,
        timestamp=datetime.now() - timedelta(days=3),
        details={"backup_filename": "old-backup.db", "bucket_name": "test"}
    )
    session.add(existing_backup)
    session.commit()
    
    job = DatabaseBackupJob(
        session=session,
        bucket_name="test-bucket", 
        file_prefix="test-backup",
        database_path=str(temp_db_file),
        backup_interval_days=7
    )
    
    job.run()
    
    # Should not create new backup or upload anything
    mock_blob.upload_from_filename.assert_not_called()
    
    # Should only have the original JobRun (no new one created)
    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 1
    assert job_runs[0].id == existing_backup.id


@patch("jobs.database_backup_job.storage.Client")
def test_backup_handles_gcp_upload_failure(mock_client_class, session, temp_db_file, mock_storage_client):
    mock_client, mock_bucket, mock_blob = mock_storage_client
    mock_client_class.return_value = mock_client
    
    mock_blob.upload_from_filename.side_effect = Exception("GCP upload failed!")
    
    job = DatabaseBackupJob(
        session=session,
        bucket_name="test-bucket",
        file_prefix="test-backup",
        database_path=str(temp_db_file)
    )
    
    with pytest.raises(Exception, match="GCP upload failed!"):
        job.run()
    
    job_runs = session.exec(select(JobRun)).all()
    assert len(job_runs) == 1
    
    job_run = job_runs[0]
    assert job_run.job_type == JobType.DATABASE_BACKUP
    assert job_run.status == JobStatus.FAILURE
    assert "GCP upload failed!" in job_run.details["error"]


@patch("jobs.database_backup_job.storage.Client")
def test_backup_calculates_database_size_correctly(mock_client_class, session, mock_storage_client):
    mock_client, mock_bucket, mock_blob = mock_storage_client
    mock_client_class.return_value = mock_client
    
    with TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        db_path.write_bytes(b"0" * (1024 * 1024))
        
        job = DatabaseBackupJob(
            session=session,
            bucket_name="test-bucket",
            file_prefix="test-backup", 
            database_path=str(db_path)
        )
        
        job.run()
        
        job_run = session.exec(select(JobRun)).first()
        details = DatabaseBackupDetails(**job_run.details)
        assert details.database_size_mb == 1.0