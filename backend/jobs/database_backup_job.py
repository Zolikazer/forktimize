from datetime import datetime, date, timedelta
from pathlib import Path

from google.cloud import storage
from sqlmodel import Session, select

from database.db import ENGINE
from model.job_run import JobRun, JobStatus, JobType, DatabaseBackupDetails
from monitoring.logging import JOB_LOGGER
from monitoring.performance import benchmark
from settings import SETTINGS


@benchmark
def run_database_backup_job():
    JOB_LOGGER.info("🔄 Running scheduled database backup job...")
    with Session(ENGINE) as session:
        DatabaseBackupJob(session).run()


class DatabaseBackupJob:
    def __init__(self,
                 session: Session,
                 bucket_name: str = SETTINGS.DATABASE_BACKUP_BUCKET_NAME,
                 file_prefix: str = SETTINGS.DATABASE_BACKUP_FILE_PREFIX,
                 database_path: str = SETTINGS.DATABASE_PATH,
                 backup_interval_days: int = SETTINGS.DATABASE_BACKUP_INTERVAL_DAYS):
        self._session = session
        self._bucket_name = bucket_name
        self._file_prefix = file_prefix
        self._database_path = Path(database_path)
        self._backup_interval_days = backup_interval_days
        self._storage_client = storage.Client()

    def run(self):
        if self._has_recent_successful_backup(self._backup_interval_days):
            JOB_LOGGER.info(f"✅ Recent backup found within {self._backup_interval_days} days, skipping...")
            return
            
        try:
            backup_date = date.today()
            backup_filename = f"{self._file_prefix}-{backup_date.strftime('%Y-%m-%d')}.db"
            
            JOB_LOGGER.info(f"📦 Starting backup: {backup_filename}")
            
            db_size_mb = self._get_database_size_mb()
            self._upload_to_storage(backup_filename)
            self._track_successful_job_run(backup_filename, backup_date, db_size_mb)
            
            JOB_LOGGER.info(f"✅ Backup completed: {backup_filename} ({db_size_mb} MB)")
            
        except Exception as e:
            self._track_failed_job_run(str(e))
            raise

    def _has_recent_successful_backup(self, days: int) -> bool:
        cutoff_time = datetime.now() - timedelta(days=days)
        
        statement = (select(JobRun)
                    .where(JobRun.job_type == JobType.DATABASE_BACKUP)
                    .where(JobRun.status == JobStatus.SUCCESS)
                    .where(JobRun.timestamp >= cutoff_time))
        
        return self._session.exec(statement).first() is not None

    def _get_database_size_mb(self) -> float:
        db_size_bytes = self._database_path.stat().st_size
        return round(db_size_bytes / (1024 * 1024), 1)

    def _upload_to_storage(self, backup_filename: str):
        bucket = self._storage_client.bucket(self._bucket_name)
        blob = bucket.blob(backup_filename)
        
        blob.upload_from_filename(str(self._database_path))

    def _track_successful_job_run(self, backup_filename: str, backup_date: date, db_size_mb: float):
        details = DatabaseBackupDetails(
            backup_filename=backup_filename,
            bucket_name=self._bucket_name,
            database_size_mb=db_size_mb,
            backup_date=backup_date
        )
        job_run = JobRun(
            job_type=JobType.DATABASE_BACKUP,
            status=JobStatus.SUCCESS,
            timestamp=datetime.now(),
            details=details.model_dump(mode='json')
        )
        self._session.add(job_run)
        self._session.commit()
        self._session.refresh(job_run)
        
        JOB_LOGGER.info(f"📌 Backup Job Run Logged: ID={job_run.id}, Status={JobStatus.SUCCESS}")

    def _track_failed_job_run(self, error_message: str):
        job_run = JobRun(
            job_type=JobType.DATABASE_BACKUP,
            status=JobStatus.FAILURE,
            timestamp=datetime.now(),
            details={"error": error_message}
        )
        self._session.add(job_run)
        self._session.commit()
        self._session.refresh(job_run)
        
        JOB_LOGGER.error(f"❌ Backup Job Run Failed: ID={job_run.id}, Error: {error_message}")


if __name__ == "__main__":
    with Session(ENGINE) as session:
        DatabaseBackupJob(session).run()