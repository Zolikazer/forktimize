import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from alembic import command
from alembic.config import Config

from monitoring.logging import APP_LOGGER
from settings import SETTINGS


def create_backup(db_path: str) -> Path | None:
    db_file = Path(db_path)

    if not db_file.exists():
        APP_LOGGER.warning(f"Database file '{db_path}' not found. Skipping backup.")
        return None

    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]  # Include microseconds, truncate to 3 digits
    backup_name = SETTINGS.DATABASE_BACKUP_LOCAL_FORMAT.format(
        stem=db_file.stem,
        timestamp=timestamp,
        suffix=db_file.suffix
    )
    backup_path = db_file.parent / backup_name
    shutil.copy(db_file, backup_path)
    APP_LOGGER.info(f"Database backup created: {backup_path}")

    return backup_path


def restore_from_backup(backup_file: Path, original_file: Path):
    if backup_file and backup_file.exists():
        shutil.copy(backup_file, original_file)
        APP_LOGGER.info("Database successfully restored from backup.")
    else:
        APP_LOGGER.critical("Backup file missing—restore failed!")


def get_backup_files(db_path: str) -> List[Path]:
    """Find all backup files for the given database, sorted newest first."""
    db_file = Path(db_path)
    # Convert creation format to search pattern by replacing {timestamp} with *
    backup_pattern = SETTINGS.DATABASE_BACKUP_LOCAL_FORMAT.format(
        stem=db_file.stem,
        timestamp="*",
        suffix=db_file.suffix
    )
    backup_files = list(db_file.parent.glob(backup_pattern))
    return sorted(backup_files, key=lambda f: f.stat().st_mtime, reverse=True)


def split_backups_by_age(backup_files: List[Path], keep_days: int) -> tuple[List[Path], List[Path]]:
    """Split backup files into recent (within keep_days) and old categories."""
    cutoff_timestamp = (datetime.now() - timedelta(days=keep_days)).timestamp()
    
    recent = [f for f in backup_files if f.stat().st_mtime >= cutoff_timestamp]
    old = [f for f in backup_files if f.stat().st_mtime < cutoff_timestamp]
    
    return recent, old


def determine_files_to_keep(recent_backups: List[Path], old_backups: List[Path], min_total: int) -> List[Path]:
    """Determine which backup files to keep based on retention policy."""
    # Always keep all recent backups
    files_to_keep = recent_backups.copy()
    
    # If we have fewer than min_total, fill up with old backups
    if len(files_to_keep) < min_total:
        additional_needed = min_total - len(files_to_keep)
        files_to_keep.extend(old_backups[:additional_needed])
    
    return files_to_keep


def delete_backup_files(files_to_delete: List[Path]):
    """Delete the specified backup files."""
    if not files_to_delete:
        APP_LOGGER.info("No old backup files to clean up.")
        return
        
    APP_LOGGER.info(f"Cleaning up {len(files_to_delete)} old backup files...")
    for backup_file in files_to_delete:
        try:
            backup_file.unlink()
            APP_LOGGER.info(f"Deleted old backup: {backup_file.name}")
        except Exception as e:
            APP_LOGGER.error(f"Failed to delete backup {backup_file.name}: {e}")


def cleanup_old_backups(db_path: str, min_backups: int = 5, keep_days: int = 14):
    """Clean up old backup files with smart retention policy."""
    backup_files = get_backup_files(db_path)
    
    if not backup_files:
        APP_LOGGER.info("No backup files found to clean up.")
        return
    
    recent_backups, old_backups = split_backups_by_age(backup_files, keep_days)
    files_to_keep = determine_files_to_keep(recent_backups, old_backups, min_backups)
    files_to_delete = [f for f in backup_files if f not in files_to_keep]
    
    delete_backup_files(files_to_delete)
    APP_LOGGER.info(f"Backup cleanup completed. Kept {len(files_to_keep)} backup files.")


def apply_migrations():
    APP_LOGGER.info("Running Alembic migrations...")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    APP_LOGGER.info("Alembic migrations completed successfully.")


def run_migrations_with_backup(db_path: str):
    db_file = Path(db_path)

    if not db_file.exists():
        APP_LOGGER.error(f"Database '{db_path}' does not exist. Migration aborted.")
        return

    backup_file = create_backup(db_path)

    try:
        apply_migrations()
        # Clean up old backups after successful migration
        cleanup_old_backups(db_path)
    except Exception as e:
        APP_LOGGER.error(f"Migration failed: {e}. Attempting to restore from backup.")
        restore_from_backup(backup_file, db_file)
        raise


if __name__ == "__main__":
    run_migrations_with_backup(sys.argv[1] if len(sys.argv) > 1 else SETTINGS.DATABASE_PATH)
