import shutil
import sys
from datetime import datetime
from pathlib import Path

from alembic import command
from alembic.config import Config

from monitoring.logging import APP_LOGGER
from settings import SETTINGS


def create_backup(db_path: str) -> Path | None:
    db_file = Path(db_path)

    if not db_file.exists():
        APP_LOGGER.warning(f"Database file '{db_path}' not found. Skipping backup.")
        return None

    backup_name = f"{db_file.parent / db_file.stem}_backup_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}{db_file.suffix}"
    shutil.copy(db_file, backup_name)
    APP_LOGGER.info(f"Database backup created: {backup_name}")

    return Path(backup_name)


def restore_from_backup(backup_file: Path, original_file: Path):
    if backup_file and backup_file.exists():
        shutil.copy(backup_file, original_file)
        APP_LOGGER.info("Database successfully restored from backup.")
    else:
        APP_LOGGER.critical("Backup file missing—restore failed!")


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
    except Exception as e:
        APP_LOGGER.error(f"Migration failed: {e}. Attempting to restore from backup.")
        restore_from_backup(backup_file, db_file)
        raise


if __name__ == "__main__":
    run_migrations_with_backup(sys.argv[1] if len(sys.argv) > 1 else SETTINGS.DATABASE_PATH)
