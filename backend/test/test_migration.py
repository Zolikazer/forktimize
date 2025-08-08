import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from migration import get_backup_files, split_backups_by_age, determine_files_to_keep, cleanup_old_backups, create_backup
from settings import SETTINGS


@pytest.fixture
def temp_db_dir():
    with TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def create_fake_backup_file(temp_dir: Path, name: str, age_days: int = 0) -> Path:
    """Create a fake backup file with specific age."""
    backup_file = temp_dir / name
    backup_file.write_text("fake backup content")
    
    # Set modification time to simulate age
    if age_days > 0:
        fake_time = datetime.now() - timedelta(days=age_days)
        timestamp = fake_time.timestamp()
        os.utime(backup_file, (timestamp, timestamp))
    
    return backup_file


def test_get_backup_files_finds_and_sorts_backups(temp_db_dir):
    db_path = str(temp_db_dir / "test.db")
    
    # Create backups with different ages (newest first in expected order)
    create_fake_backup_file(temp_db_dir, "test_backup_2025_01_03_10_00_00.db", age_days=1)
    create_fake_backup_file(temp_db_dir, "test_backup_2025_01_01_10_00_00.db", age_days=3) 
    create_fake_backup_file(temp_db_dir, "test_backup_2025_01_05_10_00_00.db", age_days=0)
    
    # Create non-backup file that should be ignored
    (temp_db_dir / "other_file.db").write_text("not a backup")
    
    backup_files = get_backup_files(db_path)
    
    assert len(backup_files) == 3
    # Should be sorted newest first
    assert backup_files[0].name == "test_backup_2025_01_05_10_00_00.db"
    assert backup_files[1].name == "test_backup_2025_01_03_10_00_00.db"
    assert backup_files[2].name == "test_backup_2025_01_01_10_00_00.db"


def test_split_backups_by_age_categorizes_correctly(temp_db_dir):
    # Create recent backup (5 days old - within 14 days)
    recent_backup = create_fake_backup_file(temp_db_dir, "recent_backup.db", age_days=5)
    
    # Create old backup (20 days old - beyond 14 days)
    old_backup = create_fake_backup_file(temp_db_dir, "old_backup.db", age_days=20)
    
    backup_files = [recent_backup, old_backup]
    recent, old = split_backups_by_age(backup_files, keep_days=14)
    
    assert len(recent) == 1
    assert len(old) == 1
    assert recent[0] == recent_backup
    assert old[0] == old_backup


def test_determine_files_to_keep_keeps_all_recent_when_enough(temp_db_dir):
    recent_backups = [
        create_fake_backup_file(temp_db_dir, f"recent_{i}.db", age_days=i) 
        for i in range(7)  # 7 recent backups
    ]
    old_backups = [
        create_fake_backup_file(temp_db_dir, f"old_{i}.db", age_days=20+i) 
        for i in range(3)  # 3 old backups
    ]
    
    files_to_keep = determine_files_to_keep(recent_backups, old_backups, min_total=5)
    
    # Should keep all 7 recent backups, no old ones
    assert len(files_to_keep) == 7
    assert all(f in recent_backups for f in files_to_keep)


def test_determine_files_to_keep_fills_up_with_old_when_not_enough_recent(temp_db_dir):
    recent_backups = [
        create_fake_backup_file(temp_db_dir, f"recent_{i}.db", age_days=i) 
        for i in range(2)  # Only 2 recent backups
    ]
    old_backups = [
        create_fake_backup_file(temp_db_dir, f"old_{i}.db", age_days=20+i) 
        for i in range(5)  # 5 old backups
    ]
    
    files_to_keep = determine_files_to_keep(recent_backups, old_backups, min_total=5)
    
    # Should keep 2 recent + 3 old = 5 total
    assert len(files_to_keep) == 5
    assert all(f in files_to_keep for f in recent_backups)
    assert sum(1 for f in old_backups if f in files_to_keep) == 3


def test_cleanup_old_backups_integration(temp_db_dir):
    db_path = str(temp_db_dir / "test.db")
    
    # Create 3 recent backups (within 14 days)
    recent_files = [
        create_fake_backup_file(temp_db_dir, f"test_backup_recent_{i}.db", age_days=i+1)
        for i in range(3)
    ]
    
    # Create 4 old backups (beyond 14 days)  
    old_files = [
        create_fake_backup_file(temp_db_dir, f"test_backup_old_{i}.db", age_days=20+i)
        for i in range(4)
    ]
    
    cleanup_old_backups(db_path, min_backups=5, keep_days=14)
    
    # Should keep all 3 recent + 2 old (to make 5 total)
    remaining_files = list(temp_db_dir.glob("test_backup_*.db"))
    assert len(remaining_files) == 5
    
    # All recent files should still exist
    for recent_file in recent_files:
        assert recent_file.exists()
    
    # Only 2 oldest files should be deleted
    deleted_count = sum(1 for old_file in old_files if not old_file.exists())
    assert deleted_count == 2


def test_cleanup_old_backups_keeps_all_when_10_recent_backups(temp_db_dir):
    db_path = str(temp_db_dir / "test.db")
    
    # Create 10 recent backups (within 14 days)
    recent_files = [
        create_fake_backup_file(temp_db_dir, f"test_backup_recent_{i}.db", age_days=i+1)
        for i in range(10)
    ]
    
    # Create 3 old backups (beyond 14 days)  
    old_files = [
        create_fake_backup_file(temp_db_dir, f"test_backup_old_{i}.db", age_days=20+i)
        for i in range(3)
    ]
    
    cleanup_old_backups(db_path, min_backups=5, keep_days=14)
    
    # Should keep all 10 recent backups and delete all old ones
    remaining_files = list(temp_db_dir.glob("test_backup_*.db"))
    assert len(remaining_files) == 10
    
    # All recent files should still exist
    for recent_file in recent_files:
        assert recent_file.exists()
    
    # All old files should be deleted
    for old_file in old_files:
        assert not old_file.exists()